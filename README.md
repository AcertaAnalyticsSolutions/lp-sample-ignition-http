# LinePulse to Ignition example using HTTP endpoint

## Background
This example shows how to send data to LinePulse from an Ignition application using Acerta's HTTP endpoint.
The following steps creates and initializes these Linux containers: 
- Ignition ver. 8.1.42
- Microsoft SQl Server database 2022-CU13-ubuntu-22.04

## Requirements
- Docker and Docker Compose should be installed

## Deployment steps

### Create secrets running the script
Linux:
```
./create_secrets.sh
```
Windows:
```
create_secrets.bat
```
### Start the containers
```
docker compose up -d
```