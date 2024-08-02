# Ignition and MS SQL database example

## Introduction
The intent of this project is to demonstrate how to send data from a Database to Acerta LinePulse platform via HTTP POST requests using Ignition Python scripts.

Inside `./ignition/projects/sample_project/ignition/script-python` there is a collection of python scripts. The one named `LinePulseAPI` exemplifies the process of acquiring a JWT token and making a request to the ingestion endpoint. The `Database` script is used to populate a MS SQL database with random data and also mark those records after the ingestion is completed.

## Requirements
- Docker and Docker Compose should be installed

## Deployment steps
The following steps create and initialize these two Linux containers: 
- Ignition ver. 8.1.42
- Microsoft SQl Server database 2022-CU13-ubuntu-22.04

### Creating secrets
Copy or rename [test.env](./test.env) to a file named: `.env`. If you don't have the client credentials, remove or comment out the `CLIENT_ID` and `CIENT_SECRET` lines, the code will automatically point to the test endpoints which don't require authentication.

### Start the containers
```
docker compose up -d
```
## Testing the application
- Navigate to the Ignition gateway page: http://127.0.0.1:9088
- It will prompt for the administrator credentials. Store this safely as they will be required if you need to log in to the gateway for any troubleshooting.
- Press the start gateway button and wait until you see the Ignition home screen
- In the `Perspective Session Launcher` section, click on the `View Projects` button
- You should see a `Acerta_Ignition_Sample` project then click on the `Lauch Project` button 
- Alternatively you can navigate to the Ignition application page directly: http://127.0.0.1:9088/data/perspective/client/sample_project

- Toggling ON `Store data` will start populating the database with simulated values every 5 seconds.
- Toggling ON `LinePulse Ingestion` will start sending the records to ingest in LinePulse every 5 seconds.
- The table will list all records that have not been ingested yet and `Records to Ingest` will show the count.
- Once a record is succesfully ingested it will be marked in the database and will not show in the table anymore.

## Troubleshooting
- Using the command: `docker ps` you should be able to verify if these two containers are running:
    - lp-sample-ignition-http-ignition-1
    - lp-sample-ignition-http-database-1
- Check the container logs for errors using `docker logs {container_name}`
- Connect to the database on port `1433` with  the `sa` credentials from the `.env` file using MS SQL Management Studio or your prefered SQL client for further investigation if required.
- Check igniton logs here: https://127.0.0.1:9088/web/status/diag.logviewer
- Ignition database connection can be verified in this address: https://127.0.0.1:9088/web/config/database.connections
- Any other configuration issues can be checked in the Ignition gateway page at http://127.0.0.1:9088.

## Terminating
Stop the containers running:
``` 
docker compose down -v
```
