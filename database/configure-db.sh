#!/bin/bash

# Wait 90 seconds for SQL Server to start up by ensuring that 
# calling SQLCMD does not return an error code, which will ensure that sqlcmd is accessible
# and that system and user databases return "0" which means all databases are in an "online" state
# https://docs.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-databases-transact-sql?view=sql-server-2017 

DBSTATUS=1
ERRCODE=1
i=0
echo "##### Waiting for MS SQL database to start  #####"
while [[ $i -lt 90 ]] && [[ $ERRCODE -ne 0 ]]; do
	i=$((i+1))
	DBSTATUS=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U SA -P $MSSQL_SA_PASSWORD -Q "SET NOCOUNT ON; Select SUM(state) from sys.databases")
	ERRCODE=$?
	sleep 1
done

if [[ $ERRCODE -ne 0 ]]; then 
	echo "SQL Server took more than 90 seconds to start up or one or more databases are not in an ONLINE state"
	exit 1
fi
echo "##### MS SQL database started, running setup script #####"
# Run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $MSSQL_SA_PASSWORD -i setup.sql