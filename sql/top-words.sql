/* Get frequent words */

--EXPLAIN QUERY PLAN
SELECT
  top.rank,
  top.freq,
  w1.*,
  "https://commons.wikimedia.org/wiki/Special:FilePath/" || w1.Hörbeispiele AS pronunciation_url
FROM
  top  JOIN words AS w1 ON w1.Wort=top.word COLLATE NOCASE
WHERE
	-- If word has multiple meanings, take first listed one
	w1.ROWID = (
		SELECT MIN(w2.ROWID)
		FROM words AS w2
		WHERE w2.Wort = top.word COLLATE NOCASE
	)
ORDER BY rank ASC
;
