#!/bin/bash

# Test the environment variables
if [[ -z "$MSSQL_SA_PASSWORD" ]]; then
    >&2 echo "MSSQL_SA_PASSWORD undefined - can't initialize the database"
    exit 1
fi

# Start the script to create the DB and user
/usr/config/configure-db.sh &

# Start SQL Server
/opt/mssql/bin/sqlservr

