
--  EXPLAIN QUERY PLAN  SELECT top.freq, nouns.* FROM nouns JOIN top ON lower(nouns.Nominativ)=top.word

--EXPLAIN QUERY PLAN
SELECT top.freq, nouns.* FROM top JOIN nouns ON nouns.Nominativ=top.word  COLLATE NOCASE
WHERE
length(nouns.Nominativ)>1  -- no single word nouns
AND substr(nouns.Nominativ,2)=lower(substr(nouns.Nominativ,2)) -- no acronymns
AND top.word NOT IN (SELECT verbs.Infinitiv FROM verbs)
ORDER BY freq DESC

--EXPLAIN QUERY PLAN
--SELECT nouns.Nominativ FROM nouns, verbs WHERE nouns.Nominativ=verbs.Infinitiv COLLATE NOCASE
