import os
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description='Do everything with German Wiktionary.')
parser.add_argument('--debug', action='store_true',
                    help='Use smaller debug file for quick testing and debugging')
args = parser.parse_args()


db_file = './db/deutsch.sqlite' if not args.debug else './db/deutsch-test.sqlite'
dump_file = './dumps/dewiktionary-latest-pages-articles.xml' if not args.debug else './dumps/dewiktionary-latest-pages-articles-test.xml'

print ('Database: {}'.format(db_file))
print ('Wiktionary Dump: {}'.format(dump_file))

# Get wiktionary dump if needed
exists = os.path.isfile(dump_file)
if not exists:
    print("Downloading wiktionary entries... (May take several minutes)")
    subprocess.run(
        ["wget", "-O", "./dumps/dewiktionary-latest-pages-articles.xml.bz2", "https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles.xml.bz2"])
    print("Decompressing wiktionary entries...(May take several minutes)")
    subprocess.run(
        ["bzip2", "-d", "./dumps/dewiktionary-latest-pages-articles.xml.bz2"])

# Directly import our top words
print("Populating db with top words...")
subprocess.run(
    ["bash", "./top/create_top_table.sh", db_file])

# Populate database
print("Parsing dump into database... (May take several minutes)")
subprocess.run(
    ["python", "./bin/dump_parse.py", "--force", "--dump", dump_file, "--db", db_file])

# Create csvs for export
print("Exporting CSV files...")
subprocess.run(
    ["bash", "sql/run_all.sh", db_file])

print("Complete!")
