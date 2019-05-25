import os
import subprocess

# Get wiktionary dump
exists = os.path.isfile('dumps/dewiktionary-latest-pages-articles.xml')
if not exists:
    print("Downloading wiktionary entries... (May take several minutes)")
    subprocess.run(
        ["wget", "-O", "./dumps/dewiktionary-latest-pages-articles.xml.bz2", "https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles.xml.bz2"])
    print("Decompressing wiktionary entries...(May take several minutes)")
    subprocess.run(
        ["bzip2", "-d", "./dumps/dewiktionary-latest-pages-articles.xml.bz2"])

# Populate database
subprocess.run(
    ["python", "./bin/dump_parse.py"])
