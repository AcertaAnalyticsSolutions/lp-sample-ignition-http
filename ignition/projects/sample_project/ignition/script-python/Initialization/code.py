import os
import sys

AUDIENCE = "https://ingestion.linepulse.ai"
CLIENT_ID = os.environ.get('CLIENT_ID','')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET','')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD','')
INGESTION_URL = "https://api.linepulse.ai/public/v1/"
INGESTOR_UUID = "d8f498e3-690e-4246-85b7-3258a719fb27"
TAGS_FILE_PATH = "/usr/local/bin/ignition/data/projects/sample_project/tags.json"
TOKEN_URL = "https://api.linepulse.ai/auth/v1/ingestion"

logger = system.util.getLogger("AcertaAPI")

def createDatabaseConnection():
	try:
		dbs = system.dataset.toPyDataSet(system.db.getConnections())
		for db in dbs:
			if db["Name"] == "acerta_db":
				return
		system.db.addDatasource(jdbcDriver="Microsoft SQLServer", name="acerta_db", description="Acerta sample database", 
			connectURL="jdbc:sqlserver://database:1433", username="sa", password=DATABASE_PASSWORD, props="databaseName=acerta_db;")
	except:
		logger.error("Database connection creation error: {}".format(str(sys.exc_info())))
	return

def createSimulatorDevice():
	try:
		devices = system.dataset.toPyDataSet(system.device.listDevices())
		for dev in devices:
			if dev["Name"] == "Acerta_Simulator":
				return
		system.device.addDevice(deviceType = "Simulator", deviceName = "Acerta_Simulator", deviceProps = {} )
	except:
		logger.error("Device creation error: {}".format(str(sys.exc_info())))
	return
	
def exportTags():
	system.tag.exportTags(filePath=TAGS_FILE_PATH, tagPaths=["[default]"])

def importTags():
	system.tag.importTags(filePath=TAGS_FILE_PATH, basePath="[default]")