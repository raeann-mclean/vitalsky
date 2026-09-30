#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE records;
    CREATE DATABASE appointments;
    CREATE DATABASE telemed;
EOSQL

#error? git update-index --chmod=+x scripts/init-multiple-dbs.sh