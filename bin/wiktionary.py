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
            m = re.search(
                "== ([a-zA-Z0-9äöüÄÖÜß \-]+?) \({{Sprache\|Deutsch}}\) ==", line)

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
            m2 = re.findall("{{Wortart\|(.+?)\|(.+?)}}", line)
            if m2:
                # Finish any existing entry
                if entry_pos:
                    yield WikEntry(page_title, entry_text, entry_pos)

                # Some words have multiple categories, we take the final one
                # E.g. Substantiv and Nachname
                # [('Substantiv', 'Deutsch'), ('Nachname', 'Deutsch')]
                entrymatch = m2[-1]

                # Skip non-german entries
                language = entrymatch[1]  # zB Deutsche, Englisch
                if language!='Deutsch':
                    entry_pos = None
                    # print ("Skipping non german: {}".format(language))
                    continue

                # Begin new entry
                entry_text = line
                entry_pos = entrymatch[0]  # zB Adverb, Substantiv

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
        self.pronunciations = list(self.get_pronunciations())
        self.translations = self.get_translations()
        self.synonyms = self.get_synonyms()
        self.antonyms = self.get_antonyms()
        self.examples = self.get_examples()
        self.verb_uebersicht = self.get_deutsch_verb_uebersicht()
        self.substantiv_uebersicht = self.get_deutsch_substantiv_uebersicht()

    def __str__(self):
        return self.title

    def uniq(self, iterator):
        """ Helper function to remove duplicates from a list, but preverving order """
        prev = None
        for item in iterator:
            if item != prev:
                prev = item
                yield item

    def strip_wikilinks(self, text):
        """
        Helper function to get rid of [[ ]] links in text
        eg 'blah [[a|b]] blah' it will return 'blah b blah'
        """
        return re.sub(r"\[\[(?:[^|\]]+\|)?([^\]]+)?\]\]", r"\1", text)

    def get_pronunciations(self, language='en'):
        """ Get audio files """
        try:
            audio_line = re.search("{{Hörbeispiele}}.*", self.text).group()
        except AttributeError:
            return []
        return self.uniq(re.findall("{{Audio\|(.+?)(?:\||}})", audio_line))


    def get_translations(self, language='en'):
        return map(self.strip_wikilinks, self.uniq(re.findall("{{Ü\|%s\|(.+?)}}" % language, self.text)))

    def get_synonyms(self):
        """ Get synonyms/Synonyme """
        try:
            section = re.search("{{Synonyme}}.*?(?:\n==|\n{{|\n\n)", self.text,
                                re.MULTILINE | re.DOTALL).group()
        except AttributeError:
            return []
        return map(self.strip_wikilinks, self.uniq(re.findall(":\[\d+] ?(.*)", section)))

    def get_antonyms(self):
        """ Get antonyms/Gegenwörter """
        try:
            section = re.search("{{Gegenwörter}}.*?(?:\n==|\n{{|\n\n)", self.text,
                                re.MULTILINE | re.DOTALL).group()
        except AttributeError:
            return []
        return map(self.strip_wikilinks, self.uniq(re.findall(":\[\d+] ?(.*)", section)))

    def get_examples(self):
        """ Get example sentences /Beispiele """
        try:
            section = re.search("{{Beispiele}}.*?(?:\n==|\n{{|\n\n)", self.text,
                       re.MULTILINE | re.DOTALL).group()
        except AttributeError:
            return []
        return map(self.strip_wikilinks, re.findall("\[\d+] ?(.*?)(?:&lt;ref|\n)", section))


    def get_template_fields(self, template_name):
        r = re.compile("{{%s(.*?)}}" % template_name,
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


    def get_deutsch_verb_uebersicht(self):
        fields = self.get_template_fields('Deutsch Verb Übersicht')
        if fields is None:
            return None
        # Check for irregular and transitive
        fields['Unreg'] = 'X' if re.search("{{unreg.}}", self.text) else ''
        fields['Trans'] = 'X' if re.search("{{trans.}}", self.text) else ''
        return fields


    def get_deutsch_substantiv_uebersicht(self):
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
