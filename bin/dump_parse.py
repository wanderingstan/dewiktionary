# Get word info from dump of wiktionary
import argparse
import sqlite3

import wiktionary


parser = argparse.ArgumentParser(description='Create database based on wiktionary dump.')
parser.add_argument('--dump',
                    default='dumps/dewiktionary-latest-pages-articles_100000.xml',
                    help='Wiktionary dump file')
parser.add_argument('--db',
                    default='db/deutsch.sqlite',
                    help='Sqlite database file')
parser.add_argument('--force', action='store_true', help='Force creation of new tables, even when they already exist.')
args = parser.parse_args()


# Get dump files at : https://dumps.wikimedia.org/dewiktionary/latest/
# args.dump = 'dumps/dewiktionary-latest-pages-articles_100000.xml'
# args.dump = 'dumps/dewiktionary-latest-pages-articles.xml'
# args.dump = 'dumps/test.xml'

# Do we force new tables to be made/
args.force = True

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

# Database
conn = sqlite3.connect(args.db)
c = conn.cursor()

# Create verb table
if args.force:
    c.execute('''DROP TABLE IF EXISTS verbs''')
german_verb_fields_sql_declarations = ",".join(
    map('"{0}" TEXT'.format, german_verb_fields)) # Put in SQL form, with text data type
c.execute('''CREATE TABLE IF NOT EXISTS verbs ("Infinitiv" TEXT, {})'''.format(
    german_verb_fields_sql_declarations))
c.execute('''CREATE INDEX verbs_index ON nouns("Infinitiv")''')

# Create noun table
if args.force:
    c.execute('''DROP TABLE IF EXISTS nouns''')
german_noun_fields_sql_declarations = ",".join(
    map('"{0}" TEXT'.format, german_noun_fields))  # Put in SQL form, with text data type
c.execute('''CREATE TABLE IF NOT EXISTS nouns ("Nominativ" TEXT, {})'''.format(
    german_noun_fields_sql_declarations))
c.execute('''CREATE INDEX nouns_index ON nouns("Nominativ")''')


# Create word table
if args.force:
    c.execute('''DROP TABLE IF EXISTS words''')
german_word_fields_sql_declarations = ",".join(
    map('"{0}" TEXT'.format, german_word_fields))  # Put in SQL form, with text data type
c.execute('''CREATE TABLE IF NOT EXISTS words ("word" TEXT PRIMARY KEY, {})'''.format(
    german_word_fields_sql_declarations))


for entry in wiktionary.read_entries(args.dump):

    print(entry.title)
    # print(entry.pos)
    # print(entry.translations())
    # print(entry.pronunciations())
    # print(entry.beispiele())

    #
    # Verbs table
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
        try:
            c.execute(sql)
        except Exception as e:
            print(e)
            print(fields)

    #
    # Nouns table
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
        try:
            c.execute(sql)
        except Exception as e:
            print (e)
            print(fields)

# Save (commit) the changes
conn.commit()
conn.close()
