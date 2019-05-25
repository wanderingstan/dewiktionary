# German Wiktionary Extraction to Sqlite and CSV

Generate useful csv files and a sqlite database from German Wiktionary.

Python3 with no dependencies.

Most recent results are in `csv` directory.

- Top words
  - [CSV](https://github.com/wanderingstan/dewiktionary/blob/master/csv/top-words.csv?raw=true)
- Top verbs 
  - [CSV](https://github.com/wanderingstan/dewiktionary/blob/master/csv/top-verbs.csv?raw=true) 
  - [Google Sheet](https://docs.google.com/spreadsheets/d/18jX0xBAx_XoUY4Uufdo1m1rLBQAJL9Mmd9I-0oc6d_g/edit?usp=sharing)
- Top nouns detailed
  - [CSV](https://github.com/wanderingstan/dewiktionary/blob/master/csv/top-nouns-detailed.csv?raw=true) 
- Top verbs detailed
  - [CSV](https://github.com/wanderingstan/dewiktionary/blob/master/csv/top-verbs-detailed.csv?raw=true) 

The resulting sqlite database will be at `./sql/deutsch.sqlite`

## Running it yourself

```
python go.py
```

Questions: stan@wanderingstan.com
