/* Get frequent words */

--EXPLAIN QUERY PLAN
SELECT
  top.rank,
  top.freq,
  w1.*,
  "https://commons.wikimedia.org/wiki/Special:FilePath/" || w1.Hörbeispiele AS pronunciation_url
FROM
  top  JOIN words AS w1 ON w1.Wort=top.word
WHERE
	-- If word has multiple meanings, take first listed one
	w1.ROWID = (
		SELECT w2.ROWID
		FROM words AS w2
		WHERE w2.Wort = top.word
        -- Nouns are our last choice. Everything has a noun form it seems!
        -- And because they're capitalized, they are on separate pages from
        -- other forms
		ORDER BY
			CASE
			   WHEN w2.Wortart="Substantiv" THEN 2
			   ELSE 1
			 END,
		w2.ROWID ASC
		LIMIT 1
	)
ORDER BY rank ASC
;
