# db location normally "./db/deutsch.sqlite"
# run from root of project
sqlite3 $1 <<EOF

.mode csv
.header on

.output ./csv/top-nouns-detailed.csv
.read ./sql/top-nouns-detailed.sql

.output ./csv/top-verbs-detailed.csv
.read ./sql/top-verbs-detailed.sql

.output ./csv/top-verbs.csv
.read ./sql/top-verbs.sql

EOF
