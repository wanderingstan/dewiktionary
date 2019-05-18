# Get word info from dump of wiktionary
import sqlite3
import re

class WikiPage:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __str__(self):
        return self.title + ' ' + self.text

    def get_template_fields(self, template_name):
        r = re.compile("\{\{%s(.*?)\}\}" % template_name,
                       re.MULTILINE | re.DOTALL)
        m = r.search(self.text)
        if m:
            fields_raw = m.group(1).split('\n|')[1:]
            field_array = list(filter(lambda x: len(x)==2, list(map(lambda f: f.replace('\n', '').split('='), fields_raw))))
            field_dict = {i[0].strip(): i[1].strip() for i in field_array}
            return field_dict
        else:
            return None

    def deutsch_verb_uebersicht(self):
        return self.get_template_fields('Deutsch Verb Übersicht')

    def deutsch_substantiv_uebersicht(self):
        return self.get_template_fields('Deutsch Substantiv Übersicht')


# Deutsch Adjektiv Übersicht
def read_wiki_entries(f):
    """ Parse a file object and return chunks for each entry """
    page_title = None
    page_text = ""
    for index, line in enumerate(f):
        if page_title is None:
            # m = re.match("    <title>(.*)</title>", line)
            m = re.search("== (.*?) \(\{\{Sprache\|Deutsch\}\}\) ==", line)

            if m:
                # Start of page
                page_title = m.group(1)

        if page_title is not None:
            m = re.search("</text>$", line)
            if m:
                # End of page
                yield WikiPage(page_title, page_text)
                # yield {'page_title': page_title, 'page_text':page_text}
                page_title = None
                page_text = ""
            else:
                # Add to page
                page_text += line


# Get dump files at : https://dumps.wikimedia.org/dewiktionary/latest/
# dump_file='dewiktionary-latest-pages-articles_100000.xml'
dump_file = 'dewiktionary-latest-pages-articles.xml'

conn = sqlite3.connect('deutsch.sqlite')
c = conn.cursor()

#
german_noun_fields = [

]

# Fields that we will record from verbs
german_verb_fields = [
    'Präsens_ich',
    'Präsens_ich*',
    'Präsens_du',
    'Präsens_du*',
    'Präsens_er, sie, es',
    'Präteritum_ich',
    'Präteritum_ich*',
    'Partizip II',
    'Partizip II*',
    'Konjunktiv II_ich',
    'Konjunktiv II_ich*',
    'Imperativ Singular',
    'Imperativ Singular*',
    'Imperativ Singular 2',
    'Imperativ Plural',
    'Imperativ Plural*',
    'Hilfsverb',
    'Hilfsverb*',
    'Bild',
    'Bild 1',
    'Bild 2',
    'Bild 3',
    'Bild 4'
]

# Create table
german_verb_fields_sql_declarations = ",".join(
    map('"{0}" TEXT'.format, german_verb_fields)) # Put in SQL form, with text data type
c.execute('''DROP TABLE IF EXISTS verbs''')
c.execute('''CREATE TABLE verbs ("Infinitiv" TEXT PRIMARY KEY, {})'''.format(
    german_verb_fields_sql_declarations))

f = open(dump_file, "r")
for entry in read_wiki_entries(f):

    raw_fields = entry.deutsch_verb_uebersicht()
    if raw_fields:
        print (entry.title)
        default_fields = {field: '' for field in german_verb_fields}
        fields = {**default_fields, **raw_fields} # Ensure all our fields have a value
        fields = {k: fields[k]
                  for k in german_verb_fields}  # Remove unknown fields
        fields['Infinitiv']=entry.title  # Title is Infinitiv form
        field_names = ','.join(map('"{0}"'.format, fields.keys()))
        field_values = ','.join(map('"{0}"'.format, fields.values()))
        sql = ('''INSERT INTO verbs (%s)\nVALUES (%s)''' % (field_names, field_values))
        try:
            c.execute(sql)
        except Exception as e:
            print (e)
            print(fields)

    # print(entry.deutsch_substantiv_uebersicht())


# Save (commit) the changes
conn.commit()
conn.close()
