/* Get frequent verbs, with all details */

-- EXPLAIN QUERY PLAN
SELECT
  top.rank, top.freq, verbs.*
FROM
  top JOIN verbs ON verbs.Infinitiv=top.word  COLLATE NOCASE
ORDER BY rank ASC, verbs.ROWID
;
