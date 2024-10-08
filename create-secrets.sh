#!/usr/bin/env bash

secrets=("client-id" "client-secret" "database-password" "gateway-admin-password")
output_file="./set_secrets.sh"

echo "#!/usr/bin/env bash" > "$output_file"

mkdir -p ./secrets

for secret in "${secrets[@]}"; do
    echo -n "Enter the value for $secret (press enter to skip): "
    read -sr value
    echo
    if [ -z "$value" ]; then
        echo "Skipping $secret..."
        continue
    fi
    echo "$value" > "./secrets/$secret"
    if [ "$secret" == "database-password" ]; then
        echo "export MSSQL_SA_PASSWORD='$value'" >> "$output_file"
    fi
done

chmod +x "$output_file"
echo "### All secrets have been set ###"
echo "Please, run the following command to generate the database password and delete the file secrets:"
echo "BASH COMMAND:"
echo "source ./$output_file && rm ./$output_file"