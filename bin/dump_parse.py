# Get word info from dump of wiktionary
import argparse
import sqlite3
import wiktionary


parser = argparse.ArgumentParser(description='Create database based on wiktionary dump.')
parser.add_argument('--dump',
                    help='Wiktionary dump file')
parser.add_argument('--db',
                    default='deutsch.sqlite',
                    help='Sqlite database file')
parser.add_argument('--force', action='store_true', help='Force creation of new tables, even when they already exist.')
args = parser.parse_args()

if args.dump is None:
    print("No dump file specified.")
    exit(0)

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
c.execute('''CREATE TABLE IF NOT EXISTS verbs ("Infinitiv" TEXT COLLATE NOCASE, {})'''.format(
    german_verb_fields_sql_declarations))
c.execute('''CREATE INDEX verbs_index ON verbs("Infinitiv")''')

# Create noun table
if args.force:
    c.execute('''DROP TABLE IF EXISTS nouns''')
german_noun_fields_sql_declarations = ",".join(
    map('"{0}" TEXT'.format, german_noun_fields))  # Put in SQL form, with text data type
c.execute('''CREATE TABLE IF NOT EXISTS nouns ("Nominativ" TEXT COLLATE NOCASE, {})'''.format(
    german_noun_fields_sql_declarations))
c.execute('''CREATE INDEX nouns_index ON nouns("Nominativ")''')

# Create word table
if args.force:
    c.execute('''DROP TABLE IF EXISTS words''')
german_word_fields_sql_declarations = ",".join(
    map('"{0}" TEXT'.format, german_word_fields))  # Put in SQL form, with text data type
c.execute('''CREATE TABLE IF NOT EXISTS words ("Wort" TEXT COLLATE NOCASE, {})'''.format(
    german_word_fields_sql_declarations))
c.execute('''CREATE INDEX word_index ON words("Wort")''')

# Create example table
if args.force:
    c.execute('''DROP TABLE IF EXISTS examples''')
c.execute('''CREATE TABLE IF NOT EXISTS examples ("words_rowid" INTEGER, "Wort" TEXT, "Beispiel")''')
c.execute('''CREATE INDEX examples_word_index ON examples("Wort")''')
c.execute('''CREATE INDEX examples_rowid_index ON examples("words_rowid")''')


for entry in wiktionary.read_entries(args.dump):

    print("\033[K\r{}".format(entry.title), end='', flush=True)

    if entry.pos == 'Nachname' or entry.pos == 'Vorname':
        # We don't care about names for now
        continue
    if entry.title.isupper():
        # We don't care about acronymns for now
        continue
    if len(entry.title)==1:
        # We don't care about 1-letter words for now
        continue

    #
    # Words table
    #
    sql = '''
        INSERT INTO words (
            'Wort',
            'Wortart',
            'Hörbeispiele',
            'Synonyme',
            'Gegenwörter',
            'Übersetzung')
        VALUES (:word, :pos, :pronunciations, :synonyms, :antonyms, :translations);
        '''
    c.execute(sql, {
        'word': entry.title,
        'pos': entry.pos,
        'pronunciations':', '.join(entry.pronunciations[:1]),
        'synonyms': ', '.join(entry.synonyms),
        'antonyms': ', '.join(entry.antonyms),
        'translations': ', '.join(entry.translations)
        })
    words_rowid = c.lastrowid # ROWID of word we just inserted

    #
    # Examples table
    #
    for example in entry.examples:
        if example.strip()=='':
            continue
        sql = '''
            INSERT INTO examples (words_rowid, Wort, Beispiel)
            VALUES (:words_rowid, :word, :example)
            '''
        c.execute(sql, {
            'words_rowid': words_rowid,
            'word': entry.title,
            'example' : example
        })

    #
    # Verbs table
    #
    raw_fields = entry.verb_uebersicht
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
    raw_fields = entry.substantiv_uebersicht
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

print("\033[K")
