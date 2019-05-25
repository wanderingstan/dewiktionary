# db location normally "../db/deutsch.sqlite"
# run from root of project (..)
sqlite3 $1 <<EOF
DROP TABLE IF EXISTS top;
CREATE TABLE top (word TEXT PRIMARY KEY, freq INT);
.mode csv
.import ./top-words/top-words-lemmetized.csv "top"

ALTER TABLE top ADD rank INT;

WITH cte AS (SELECT *, ROW_NUMBER() OVER() AS rn FROM "top")
UPDATE "top" SET rank = (SELECT rn FROM cte WHERE cte.word = top.word);
EOF
