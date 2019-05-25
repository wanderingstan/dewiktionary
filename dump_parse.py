# Get word info from dump of wiktionary
import sqlite3

import wiktionary


# Fields that we will reocrd from nouns
german_noun_fields = [
    'Genus',
    'Nominativ Singular',
    'Nominativ Plural',
    'Genitiv Singular',
    'Genitiv Plural',
    'Dativ Singular',
    'Dativ Plural',
    'Akkusativ Singular',
    'Akkusativ Plural',
    'Bild',
    'Bild 1',
    'Bild 2',
    'Bild 3',
    'Bild 4'
]

# Fields that we will record from verbs
german_verb_fields = [
    'Unreg',
    'Trans',
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

german_word_fields = [
    'Wortart',
    'Hörbeispiele',
    'Synonyme',
    'Gegenwörter',
    'Übersetzung',

]

# Get dump files at : https://dumps.wikimedia.org/dewiktionary/latest/
dump_file='dewiktionary-latest-pages-articles_100000.xml'
# dump_file = 'dewiktionary-latest-pages-articles.xml'
# dump_file = 'test.xml'

database_filename='deutsch.sqlite'



# Database
conn = sqlite3.connect(database_filename)
c = conn.cursor()

# # Create verb table
# german_verb_fields_sql_declarations = ",".join(
#     map('"{0}" TEXT'.format, german_verb_fields)) # Put in SQL form, with text data type
# c.execute('''DROP TABLE IF EXISTS verbs''')
# c.execute('''CREATE TABLE verbs ("Infinitiv" TEXT PRIMARY KEY, {})'''.format(
#     german_verb_fields_sql_declarations))

# # Create noun table
# german_noun_fields_sql_declarations = ",".join(
#     map('"{0}" TEXT'.format, german_noun_fields))  # Put in SQL form, with text data type
# c.execute('''DROP TABLE IF EXISTS nouns''')
# c.execute('''CREATE TABLE nouns ("Nominativ" TEXT PRIMARY KEY, {})'''.format(
#     german_noun_fields_sql_declarations))

# Create word table
# german_word_fields_sql_declarations = ",".join(
#     map('"{0}" TEXT'.format, german_word_fields))  # Put in SQL form, with text data type
# c.execute('''DROP TABLE IF EXISTS words''')
# c.execute('''CREATE TABLE words ("word" TEXT PRIMARY KEY, {})'''.format(
#     german_word_fields_sql_declarations))


for entry in wiktionary.read_entries(dump_file):

    print(entry.title, entry.pos)

    # print(entry.translations())
    print(entry.audio())

    #
    # Verbs
    #
    raw_fields = entry.deutsch_verb_uebersicht()
    if raw_fields:
        default_fields = {field: '' for field in german_verb_fields}
        # unknown_fields = list(filter(lambda f: f not in default_fields, raw_fields.keys()))
        # print(unknown_fields)
        fields = {**default_fields, **raw_fields} # Ensure all our fields have a value
        fields = {k: fields[k]
                  for k in german_verb_fields}  # Remove unknown fields
        fields['Infinitiv']=entry.title  # Title is Infinitiv form
        field_names = ','.join(map('"{0}"'.format, fields.keys()))
        field_values = ','.join(map('"{0}"'.format, fields.values()))
        sql = ('''INSERT INTO verbs (%s)\nVALUES (%s)''' % (field_names, field_values))
        # try:
        #     c.execute(sql)
        # except Exception as e:
        #     print(e)
        #     print(fields)
    #
    # Nouns
    #
    raw_fields = entry.deutsch_substantiv_uebersicht()
    if raw_fields:
        default_fields = {field: '' for field in german_noun_fields}
        # unknown_fields = list(filter(lambda f: f not in default_fields, raw_fields.keys()))
        # print(unknown_fields)
        fields = {**default_fields, **raw_fields} # Ensure all our fields have a value
        fields = {k: fields[k]
                  for k in german_noun_fields}  # Remove unknown fields
        fields['Nominativ'] = entry.title  # Title is Nominativ form
        field_names = ','.join(map('"{0}"'.format, fields.keys()))
        field_values = ','.join(map('"{0}"'.format, fields.values()))
        sql = ('''INSERT INTO nouns (%s)\nVALUES (%s)''' % (field_names, field_values))
        # try:
        #     c.execute(sql)
        # except Exception as e:
        #     print (e)
        #     print(fields)

# Save (commit) the changes
conn.commit()
conn.close()
