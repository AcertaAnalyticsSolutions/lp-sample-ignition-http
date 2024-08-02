import uuid
import sys
from datetime import datetime
logger = system.util.getLogger("AcertaAPI")

def saveDataToDatabase(tagPath):
	enableSimulation = system.tag.readBlocking("[default]EnableDataSimulation")[0].value
	if enableSimulation:
		params = {
		"measuredAt" : system.date.now(),
		"value" :system.tag.readBlocking(tagPath)[0].value,
		"highLimit" : system.tag.readBlocking(tagPath + ".EngHigh")[0].value,
		"lowLimit" : system.tag.readBlocking(tagPath + ".EngLow")[0].value,
		"modelNumber" : "123456789",
		"testResult" : 1,
		"color" : "BLUE",
		"size" : "LARGE",
		"shift" : 1,
		"partId" : "AZ12345",
		"station" : "Conveyor South",
		"line" : "Nuts Assembly",
		"signalName" : system.tag.readBlocking(tagPath + ".Name")[0].value,
		"recordId" : str(uuid.uuid4())
		}
		result = system.db.runNamedQuery("InsertDemoData", params)

def updateIngestedTimestamp(records_id):
	try:
		records_str = ""
		for record in records_id:
			records_str = records_str + "'" + str(record) + "',"
		records_str = records_str[:-1]
		params = {
		"ingestedAt" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		"recordIds" : records_str
		}
		logger.info("Updating record timestamp - records:{}".format(params))
		result = system.db.runNamedQuery(project="sample_project", path="UpdateIngestedTimestamp", parameters=params)
		logger.info("DB updated - result: {}".format(result))
	except:
		logger.error("Failed to update ingested timestamp - error: {}".format(str(sys.exc_info())))