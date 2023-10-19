import paho.mqtt.client as mqtt
import datetime
import threading
from finite_scan import mainFiniteScan
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import schedule
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("RPI")
autoConfDict = {'Timer':24}
sensorParamDict = {'SAMPLERATE': 200, 'SAMPLEDURATION': 300, 'SENSITIVITY': 500}
metaData = {}

def uploadToCloud(metaData):
    uri = "mongodb+srv://admin:W176xRINyYUOZCKE@cluster0.r000trc.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Cluster0']
    collection = db['Accl_Data']
    csv_data = pd.read_csv('./main.csv')
    document = {'metadata': metaData,'csv_data': csv_data.to_dict(orient='list')}
    collection.insert_one(document)
    print("Success: Data uploaded to MongoDB")
    
def decode_messgae(text,time):
    if text == "START":
        print("STARTING REMOTE SENSING JOB")
        actual_scan_rate, metaData = mainFiniteScan(sensorParamDict)
        print("Actual Scan Rate: ", actual_scan_rate)
        client.publish("RETURNSCANRATE", actual_scan_rate)
        thread3 = threading.Thread(target=uploadToCloud, args=(metaData,))
        thread3.start()
    elif text == "CHECK":
        client.publish("SENSOR", str(sensorParamDict))
    elif text == "HISTORY":
        with open("./logFile.txt", 'r') as file:
            lines = file.readlines()
        num_lines_to_read = 10
        last_lines = [line.strip() for line in lines[-num_lines_to_read:]]
        client.publish("HISTORY", str(last_lines))
    elif text == "12":
        autoConfDict['Timer'] = 12
    elif text == "24":
        autoConfDict['Timer'] = 24
    elif text == "48":
        autoConfDict['Timer'] = 48
    else:
        lst = text.split(':')
        sensorParamDict[lst[0]] = lst[1]
        print(sensorParamDict)

def on_message(client, userdata, message):
    current_time = datetime.datetime.now().time()
    print("Received message:", str(message.payload.decode("utf-8")), str(current_time))
    decode_messgae(str(message.payload.decode("utf-8")),str(current_time))


def main():
    print("Running remote sensing")
    client.connect(mqttBroker)
    client.on_message = on_message
    client.subscribe("REMOTE SENSING")
    client.loop_forever()

def main2():
    def run_scan():
        actual_scan_rate, metaData = mainFiniteScan(sensorParamDict)
    while True:
        value = autoConfDict['Timer']
        if value is not None:
            schedule.every(value).hours.do(run_scan)
        schedule.run_pending()
        time.sleep(1)
    
thread1 = threading.Thread(target=main)
thread2 = threading.Thread(target=main2)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Program Exit")





