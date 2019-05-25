# Export csv of top verbs

sqlite3 ../wiktionary/deutsch.sqlite <<EOF
.mode csv
.output top-verbs.csv
SELECT
  ROW_NUMBER() OVER (ORDER BY top.freq DESC) AS rank,
  top.freq,
  verbs."Infinitiv",
  verbs."Unreg",
  verbs."Trans",
  verbs."Präsens_ich",
  verbs."Präsens_du",
  verbs."Präsens_er, sie, es",
  verbs."Präteritum_ich",
  verbs."Partizip II",
  verbs."Konjunktiv II_ich",
  verbs."Imperativ Singular",
  verbs."Imperativ Plural",
  verbs."Hilfsverb"
FROM
  top, verbs
WHERE
  top.word=verbs.Infinitiv;
.quit

EOF
echo "Exported top-verbs.csv"
