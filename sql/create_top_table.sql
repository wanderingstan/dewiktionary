DROP TABLE top
;
CREATE TABLE top (word TEXT PRIMARY KEY, freq INT)
;
.mode csv
.import "./top/top-words-lemmetized.csv" "top"


-- Add rank column and populate
ALTER TABLE top ADD rank INT
;
WITH cte AS (SELECT *, ROW_NUMBER() OVER() AS rn FROM "top")
UPDATE "top" SET rank = (SELECT rn FROM cte WHERE cte.word = top.word)
;
