# Get word info from dump of wiktionary
import argparse
import sqlite3
import wiktionary

parser = argparse.ArgumentParser(description='Test parsing.')
parser.add_argument('--dump',
                    default='./dumps/dewiktionary-latest-pages-articles-test.xml',
                    help='Wiktionary dump file')
args = parser.parse_args()

for entry in wiktionary.read_entries(args.dump):

    print(entry.title)
    # print(entry.pos)
    # print(entry.translations())
    # print(entry.pronunciations())
    # print(entry.beispiele())
    print(list(entry.synonyms))
    print(list(entry.antonyms))


