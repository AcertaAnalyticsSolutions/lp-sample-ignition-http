# LinePulse to Ignition example using HTTP endpoint

## Introduction
This example shows how to send data to LinePulse from an Ignition application using Acerta's HTTP endpoint.
The following steps create and initializes these Linux containers: 
- Ignition ver. 8.1.42
- Microsoft SQl Server database 2022-CU13-ubuntu-22.04

## Requirements
- Docker and Docker Compose should be installed

## Deployment steps

### Create secrets running the script
#### Linux:
```
./create_secrets.sh
```
After the secrets are created, run this:
```
source ././set_secrets.sh && rm ././set_secrets.sh
```
#### Windows:
```
create_secrets.bat
```
After the secrets are created, run this:
```
call set_secrets.bat && del set_secrets.bat
```
### Start the containers
```
docker compose up -d
```
## Testing the application
- Navigate to the Ignition application page: http://127.0.0.1:9088/data/perspective/client/sample_project

- Toggling ON `Store data` will start populating the database with simulated values every 5 seconds.
- Toggling ON `LinePulse Ingestion` will start sending the records to ingest in LinePulse every 5 seconds.
- The table will list all records that have not been ingested yet and `Records to Ingest` will show the count.
- Once a record is succesfully ingested it will be marked in the database and will not show in the table anymore.

## Troubleshooting
- Using the command: `docker ps` you should be able to verify if these two containers running:
    - lp-sample-ignition-http-ignition-1
    - lp-sample-ignition-http-database-1
- Check the container logs for errors using `docker logs {container_name}`
- Connect to the database on port `1433` using MS SQL Management Studio or your prefered GUI tool for further investigation if required.
- Navigate to the Ignition gateway at http://127.0.0.1:9088 to verify any required configuration, such as the database connection, logs, etc. Requires login with the user `admin` and the password created in the previous steps.

## Terminating
Stop the containers running:
``` 
docker compose down -v
```
