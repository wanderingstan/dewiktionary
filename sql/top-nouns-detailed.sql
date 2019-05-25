/* Get frequent nouns, with all details */

-- EXPLAIN QUERY PLAN

SELECT
  top.rank, top.freq, nouns.*
FROM
  top JOIN nouns ON nouns.Nominativ=top.word  COLLATE NOCASE
WHERE
  length(nouns.Nominativ)>1  -- no single word nouns
AND
  top.word NOT IN (SELECT verbs.Infinitiv FROM verbs)  -- not also a verb
-- AND substr(nouns.Nominativ,2)=lower(substr(nouns.Nominativ,2)) AND -- no acronymns (Causes table scan, why?)
ORDER BY rank ASC, nouns.ROWID
;
