import datetime
import schedule
import time
import paho.mqtt.client as mqtt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from finite_scan import mainFiniteScan
import pandas as pd

time.sleep(60)
mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("RPINode1")
autoConfDict = {'Timer': 3}
sensorParamDict = {'SAMPLERATE': 200, 'SAMPLEDURATION': 10, 'SENSITIVITY0': 500, 'SENSITIVITY1': 500}
metaData = {"RPI Number" : 1}


def uploadToCloud(metaData):
    uri = "mongodb+srv://admin:W176xRINyYUOZCKE@cluster0.r000trc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Cluster0']
    collection = db['Accl_Data']
    metaData["RPI Number"] = 1
    csv_data = pd.read_csv('./main.csv')
    document = {'metadata': metaData, 'csv_data': csv_data.to_dict(orient='list')}
    collection.insert_one(document)
    print("Success: Data uploaded to MongoDB")


def decode_messgae(text, time):
    print(text)
    if text == "START":
        print("STARTING REMOTE SENSING JOB")
        actual_scan_rate, metaData = mainFiniteScan(sensorParamDict)
        print("Actual Scan Rate: ", actual_scan_rate)
        client.publish("RETURNSCANRATE1", actual_scan_rate)
        uploadToCloud(metaData)
    elif text == "CHECK":
        client.publish("SENSOR1", str(sensorParamDict))
    elif text == "HISTORY":
        with open("./logFile.txt", 'r') as file:
            lines = file.readlines()
        num_lines_to_read = 10
        last_lines = [line.strip() for line in lines[-num_lines_to_read:]]
        client.publish("HISTORY1", str(last_lines))
    elif text == "RESETAUTO":
        schedule.clear()
        schedule.every(autoConfDict["Timer"]).hours.do(upload_job)
    elif text == "RESETREMOTE":
        print("STARTING REMOTE SENSING JOB")
        actual_scan_rate, metaData = mainFiniteScan(sensorParamDict)
        print("Actual Scan Rate: ", actual_scan_rate)
        uploadToCloud(metaData)
    elif text in {"12", "24", "48"}:
        autoConfDict['Timer'] = int(text)
    else:
        lst = text.split(':')
        sensorParamDict[lst[0]] = lst[1]
        print(sensorParamDict)


def on_message(client, userdata, message):
    current_time = datetime.datetime.now().time()
    print("Received message:", str(message.payload.decode("utf-8")), str(current_time))
    decode_messgae(str(message.payload.decode("utf-8")), str(current_time))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("REMOTE SENSING1")
    else:
        print(f"Connection failed with result code {rc}")
        time.sleep(5)


def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}. Reconnecting...")

    while not client.is_connected():
        try:
            client.reconnect()
        except Exception as e:
            print(f"Reconnection failed: {str(e)}")
            time.sleep(5)

    print("Reconnected successfully")


client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("Running remote sensing")
client.connect(mqttBroker)


def main():
    client.loop_start()
    while True:
        schedule.run_pending()
        time.sleep(1)


def upload_job():
    actual_scan_rate, metaData = mainFiniteScan(sensorParamDict)
    uploadToCloud(metaData)


schedule.every(autoConfDict["Timer"]).hours.do(upload_job)

main()





