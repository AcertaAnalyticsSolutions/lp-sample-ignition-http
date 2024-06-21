#!/bin/bash

secrets=("client_id" "client_secret" "database_password" "gateway-admin-password")

mkdir -p ./secrets

for secret in "${secrets[@]}"; do
    read -sp "Enter the value for $secret (press enter to skip): " value
    echo
    if [ -z "$value" ]; then
        echo "Skipping $secret..."
        continue
    fi
    if [ "$secret" == "database_password" ]; then
        export MSSQL_SA_PASSWORD=$value
    fi
    echo $value > ./secrets/$secret
    
done