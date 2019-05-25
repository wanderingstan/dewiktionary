/* Get frequent verbs, with most common conjugations */

-- EXPLAIN QUERY PLAN
SELECT
  top.rank,
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
  top JOIN verbs ON verbs.Infinitiv=top.word  COLLATE NOCASE
ORDER BY rank ASC
;
