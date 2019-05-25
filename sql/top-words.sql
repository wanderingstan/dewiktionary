/* Get frequent words */

-- EXPLAIN QUERY PLAN
SELECT
  top.rank,
  top.freq,
  words.*,
  "https://commons.wikimedia.org/wiki/Special:FilePath/" || words.Hörbeispiele AS pronunciation_url
FROM
  top JOIN words ON words.Wort=top.word COLLATE NOCASE
ORDER BY rank ASC
;
