@echo off
setlocal enabledelayedexpansion

set "secrets=client-id client-secret database-password gateway-admin-password"
set "output_file=set_secrets.bat"

echo @echo off > "%output_file%"

if not exist secrets (
    mkdir secrets
)

for %%s in (%secrets%) do (
    set "secret=%%s"
    set /p "value=Enter the value for !secret! (press enter to skip): "
    if "!value!"=="" (
        echo Skipping !secret!...
    ) else (
        echo !value! > "secrets\!secret!"
        if "!secret!"=="database-password" (
            echo set MSSQL_SA_PASSWORD=!value! >> "%output_file%"
        )
    )
)

echo ### All secrets have been set ###
echo Please, run the following command to generate the database password and delete the file secrets:
echo BATCH COMMAND:
echo call %output_file% ^&^& del %output_file%