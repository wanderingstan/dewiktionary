# db location normally "../db/deutsch.sqlite"
# run from root of project (..)
sqlite3 $1 <<EOF
.read ./sql/create_top_table.sql
EOF
