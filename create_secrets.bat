@echo off
setlocal enabledelayedexpansion

set secrets="client_id" "client_secret" "database_password" "gateway-admin-password"

if not exist secrets mkdir secrets

for %%s in (%secrets%) do (
    set /p value="Enter the value for %%s: "
    if "%%s"=="database_password" (
        setx MSSQL_SA_PASSWORD !value!
    ) else (
        echo !value! > secrets\%%s
    )
)