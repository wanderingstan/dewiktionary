import re


def read_entries(dump_file):
    """
    Parse a file object and return WikEntry object for each entry
    Note that one page can have multiple entries, for different parts of speech.
    """
    f = open(dump_file, "r")
    page_title = None
    entry_pos = None
    entry_text = ""
    for index, line in enumerate(f):
        if page_title is None:
            # m = re.match("    <title>(.*)</title>", line)
            m = re.search("== (.*?) \(\{\{Sprache\|Deutsch\}\}\) ==", line)

            if m:
                # Start of entry
                page_title = m.group(1)
                entry_pos = None
                entry_text = ""
                continue

        if page_title is not None:
            # We are in a page

            # Test for end of page
            m = re.search("</text>$", line)
            if m:
                # Finish any existing entry
                if entry_pos:
                    yield WikEntry(page_title, entry_text, entry_pos)
                page_title = None
                entry_pos = None
                entry_text = ""
                continue

            # Test for new entry
            m2 = re.search("\{\{Wortart\|(.+?)\|(.+?)\}\}", line)
            if m2:
                # Finish any existing entry
                if entry_pos:
                    yield WikEntry(page_title, entry_text, entry_pos)

                # Skip non-german entries
                language = m2.group(2) # zB Deutsche, Englisch
                if language!='Deutsch':
                    entry_pos = None
                    print ("Skipping non german: {}".format(language))
                    continue

                # Begin new entry
                entry_text = line
                entry_pos = m2.group(1) # zB Adverb, Substantiv

            if entry_pos is None:
                # We're on a page, but in an entry for another language or something.
                continue

            # Regular line, add to current entry
            entry_text += line



class WikEntry:
    """ Class representing a german wiktionary entry """

    def __init__(self, title, text, pos):
        self.title = title
        self.text = text
        self.pos = pos
        self.verb_uebersicht = self.deutsch_verb_uebersicht()
        self.substantiv_uebersicht = self.deutsch_substantiv_uebersicht()
        self.translations = self.translations()


    def __str__(self):
        return self.title


    def pronunciations(self, language='en'):
        """ Get audio files """
        try:
            audio_line = re.search("\{\{Hörbeispiele\}\}.*", self.text).group()
        except AttributeError:
            return []
        return re.findall("\{\{Audio\|(.+?)(?:\||\}\})", audio_line)


    def translations(self, language='en'):
        return re.findall("\{\{Ü\|%s\|(.+?)\}\}" % language, self.text)


    def beispiele(self):
        """ Get example sentences """
        try:
            section = re.search("\{\{Beispiele\}\}.*?(?:\n==|\n\{\{|\n\n)", self.text,
                       re.MULTILINE | re.DOTALL).group()
        except AttributeError:
            return []
        return re.findall("\[\d+] ?(.*?)(?:&lt;ref|\n)", section)


    def get_template_fields(self, template_name):
        r = re.compile("\{\{%s(.*?)\}\}" % template_name,
                       re.MULTILINE | re.DOTALL)
        m = r.search(self.text)
        if m:
            fields_raw = m.group(1).split('\n|')[1:]
            # Some listing have various dashes to indicate "nothing"
            field_array = list(filter(lambda x: len(x) == 2, list(
                map(lambda f: f.replace('\n', '').replace('—', '').replace('—','').split('='), fields_raw))))
            field_dict = {i[0].strip(): i[1].strip() for i in field_array}
            return field_dict
        else:
            return None


    def deutsch_verb_uebersicht(self):
        fields = self.get_template_fields('Deutsch Verb Übersicht')
        if fields is None:
            return None
        # Check for irregular and transitive
        fields['Unreg'] = 'X' if re.search("\{\{unreg.\}\}", self.text) else ''
        fields['Trans'] = 'X' if re.search("\{\{trans.\}\}", self.text) else ''
        return fields


    def deutsch_substantiv_uebersicht(self):
        fields = self.get_template_fields('Deutsch Substantiv Übersicht')
        if fields is None:
            return None
        # Special case for multiple genders. We concat and sort them them, e.g. 'fm'
        if 'Genus 1' in fields and 'Genus 2' in fields:
            fields['Genus'] = ''.join(
                sorted(fields['Genus 1'] + fields['Genus 2']))
        # Field substitutions, cuz humans are inconsistant in naming
        # Later might include the '2' and '*' fields.
        field_subs = {
            'Nominativ Plural 1': 'Nominativ Plural',
            'Genitiv Plural 1': 'Genitiv Plural',
            'Dativ Plural 1': 'Dativ Plural',
            'Akkusativ Plural 1': 'Akkusativ Plural',
            'Nominativ Singular 1': 'Nominativ Singular',
            'Dativ Singular 1': 'Dativ Singular',
            'Akkusativ Singular 1': 'Akkusativ Singular'
        }
        fields_2 = {
            field_subs[k] if k in field_subs else k: v for k, v in fields.items()}
        return fields_2
