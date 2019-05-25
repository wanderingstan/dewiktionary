import os
import subprocess

db_file = './db/deutsch.sqlite'

# Get wiktionary dump if needed
exists = os.path.isfile('dumps/dewiktionary-latest-pages-articles.xml')
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
    ["python", "./bin/dump_parse.py", "--force", "--dump", "dumps/dewiktionary-latest-pages-articles.xml", "--db", db_file])

# Create csvs for export
print("Exporting CSV files...")
subprocess.run(
    ["bash", "sql/run_all.sh", db_file])

print("Complete!")
