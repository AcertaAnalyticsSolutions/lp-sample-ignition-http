import sys
import json

client = system.net.httpClient()
logger = system.util.getLogger("AcertaAPI")

def getAcertaToken(audience=Initialization.AUDIENCE, client_id=Initialization.CLIENT_ID, client_secret=Initialization.CLIENT_SECRET, ingestor_uuid=Initialization.INGESTOR_UUID):
	if (not client_id and not client_secret):
		logger.info("No client_id or client_secret provided, running in test mode")
		return
	try:
		body = {"grant_type": "client_credentials",
				"audience": audience,
				"client_secret": client_secret,
				"client_id": client_id,
				"ingestor_uuid": ingestor_uuid }
		#logger.info("Sending token request - body: {}".format(body))
		response = client.post(url=tokenUrl, data=body)
		logger.info("token response: {}".format(response))
		if response.isGood():
			responseBody = response.getJson()
			return responseBody["access_token"]
	except:
		logger.error("Failed to get a token - error: {}".format(str(sys.exc_info())))
		
		
token = getAcertaToken()


def sendLinePulseHTTPRequest(tagPath, token=None, ingestionUrl=Initialization.INGESTION_URL):
	records_id = []
	headers = {}
	def callbackHTTPRequest(response, error):
		LinePulseAPI.updateIngestedRecords(response, error, records_id)
	
	try:
		data, records_id = datasetToIngestionRecord(tagPath)
		if not token:
			ingestionUrl = ingestionUrl + "test/"
		else:
			headers = {"Authorization": "Bearer " + token}
		logger.info("Sending request to LinePulse - data: {} - url: {}".format(data, ingestionUrl))
		request = client.postAsync(url=ingestionUrl + "ingestion/ingestors/" + Initialization.INGESTOR_UUID + "/record", headers=headers, data=data)
		request.whenComplete(callbackHTTPRequest)
		logger.info("Request sent: {}".format(str(request)))
	except:
		logger.error("Failed trying to send HTTP data to LP: {}".format(str(sys.exc_info())))

def updateIngestedRecords(response, error, records_id):
	if response and response.isGood():
		logger.info("Received response from LinePulse: {} - records: {}".format(str(response), records_id))
		Database.updateIngestedTimestamp(records_id)
	else:
		logger.error("Received error from LinePulse - response: {} - error: {} ".format(str(response.getText()), str(error)))

def datasetToIngestionRecord(tagPath, numberOfRows=1):
	tagName = system.tag.getConfiguration(tagPath, False)[0]['name']
	tagValue = system.tag.readBlocking(tagPath)[0].value
	tagDict = json.loads(system.util.jsonEncode(tagValue))
	columns = tagValue.getColumnNames()
	records = []
	record_ids = []
	for row in tagDict["rows"]:
	    record = dict(zip(columns, row))
	    record_ids.append(record["recordId"])
	    records.append(record)
	    if len(records) >= numberOfRows:
	    	break
	payload = {
		"dataSources": [
			{
				"name": tagName,
				"records": records
			}
		]
	}
	return payload, record_ids

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