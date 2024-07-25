import os
import sys
import time

client = system.net.httpClient()
logger = system.util.getLogger("AcertaAPI")

audience = os.environ.get('AUDIENCE','https://ingestion.linepulse.ai')
clientId = ''
clientSecret = ''
databasePassword = ''
ingestionUrl = os.environ.get('INGESTION_URL', 'https://ingestion.linepulse.ai/v1/data_json')
ingestorUuid = os.environ.get('INGESTOR_UUID','')
tagsFilePath = "/usr/local/bin/ignition/data/projects/sample_project/tags.json"
token = ''
tokenUrl = os.environ.get('TOKEN_URL', 'https://api.linepulse.ai/auth/v1/ingestion')

def initializeSecrets():
	try:
		global clientId 
		clientId = system.file.readFileAsString(os.environ.get('CLIENT_ID_FILE','')).strip()
		global clientSecret 
		clientSecret = system.file.readFileAsString(os.environ.get('CLIENT_SECRET_FILE','')).strip()
		global databasePassword 
		databasePassword = system.file.readFileAsString(os.environ.get('DATABASE_PASSWORD_FILE','')).strip()
		global token
		token = getAcertaToken()
		#logger.debug("Secrets initialized - client: {} - secret: {} - db password: {} - token: {}".format(clientId, clientSecret, databasePassword, token))
	except IOError:
		logger.error("Secret files not found")
	return

def createDatabaseConnection():
	try:
		dbs = system.dataset.toPyDataSet(system.db.getConnections())
		for db in dbs:
			if db["Name"] == "acerta_db":
				return
		system.db.addDatasource(jdbcDriver="Microsoft SQLServer", name="acerta_db", description="Acerta sample database", 
			connectURL="jdbc:sqlserver://database:1433", username="sa", password=databasePassword, props="databaseName=acerta_db;")
	except:
		logger.error("Database connection creation error: {}".format(str(sys.exc_info())))
	return

def createSimulatorDevice():
	system.device.addDevice(deviceType = "Simulator", deviceName = "Acerta_Simulator", deviceProps = {} )

def exportTags():
	system.tag.exportTags(filePath=tagsFilePath, tagPaths=["[default]"])

def importTags():
	system.tag.importTags(filePath=tagsFilePath, basePath="[default]")

def getAcertaToken():
	try:
		body = {"grant_type": "client_credentials",
				"audience": audience,
				"client_secret": clientSecret,
				"client_id": clientId,
				"ingestor_uuid": ingestorUuid }
		#logger.info("Sending token request - body: {}".format(body))
		response = client.post(url=tokenUrl, data=body)
		logger.info("token response: {}".format(response))
		if response.isGood():
			responseBody = response.getJson()
			return responseBody["access_token"]
	except:
		logger.error("Failed to get a token - error: {}".format(str(sys.exc_info())))

def sendLinePulseHTTPRequest(tagPath):
	records_id = []
	
	def callbackHTTPRequest(response, error):
		LinePulseAPI.updateIngestedRecords(response, error, records_id)
	
	try:
		data, records_id = datasetToSparkplugBJson(tagPath)
		headers = {"Authorization":"Bearer " + token}
		logger.info("Sending request to LinePulse - data: {}".format(data))
		request = client.postAsync(url=ingestionUrl, params={"ingestor_uuid": ingestorUuid}, headers=headers, data=data)
		request.whenComplete(callbackHTTPRequest)
		logger.info("Request sent: {}".format(str(request)))
	except:
		logger.error("Failed trying to send HTTP data to LP: {}".format(str(sys.exc_info())))

def updateIngestedRecords(response, error, records_id):
	if response and response.isGood():
		logger.info("Received response from LinePulse: {} - records: {}".format(str(response), records_id))
		Simulation.updateIngestedTimestamp(records_id)
	else:
		logger.error("Received error from LinePulse - response: {} - error: {} ".format(str(response.getText()), str(error)))

def datasetToSparkplugBJson(tagPath, numberOfRows=1):
	
	config = system.tag.getConfiguration(tagPath, False)[0]
	dataset = system.tag.readBlocking(tagPath)[0]
	pyData = system.dataset.toPyDataSet(dataset.value)
	columns = dataset.value.getColumnNames()
	types = ["string"] * len(columns)
	records_id = []
    # Create the Sparkplug B dataset structure
	sparkplug_payload = {
	    "payload": {
	        "metrics": [
	            {
	                "dataType": "DataSet",
	                "name": config['name'],
	                "timestamp": system.date.format(system.date.now(),"yyyy-MM-dd'T'HH:mm:ss"),
	                "value": {
	                    "columnNames": list(columns),
	                    "numberOfColumns": len(columns),
	                    "rows": [],
	                    "types": types
	                }
	            }
	        ],
	        "seq": 1,
	        "timestamp": system.date.format(system.date.now(),"yyyy-MM-dd'T'HH:mm:ss")
	    },
	    "payload_row_count": len(pyData)
	}
	
	for row in pyData:
	    sparkplug_row = []
	    for col in columns:
	        value = row[col]
	        if isinstance(value, (int, float)):
	            sparkplug_row.append(value)
	        else:
	            sparkplug_row.append(str(value))
	    else:
	        sparkplug_payload["payload"]["metrics"][0]["value"]["rows"].append(sparkplug_row)
	        records_id.append(row["recordId"])
	        if (len(sparkplug_payload["payload"]["metrics"][0]["value"]["rows"]) >= numberOfRows):
	        	break
	return sparkplug_payload, records_id