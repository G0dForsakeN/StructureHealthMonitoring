import paho.mqtt.client as mqtt
import datetime
import threading
import time

# Sampling Rate: 200-5000, integer, default: 200
# Sensitivity: 400-600, integer, default: 500
# Sampling Duration: 10s-600s, integer, default: 300

# 2 x a day
# 57 minutes
# 8 channels of data
# 200 hz
# 1 month
mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Client")
client.connect(mqttBroker)
def on_message1(client, userdata, message):
    print(f"Received message - Actual Scan Rate: {message.payload.decode()}")
    main()

def mqtt_client_thread1(client):
    client.on_message = on_message1
    client.subscribe("RETURNSCANRATE")
    client.loop_forever()

def checkSampl():
    sensor_client = mqtt.Client("SampleClient")
    sensor_client.connect(mqttBroker)
    mqtt_thread = threading.Thread(target=mqtt_client_thread1, args=(sensor_client,))
    mqtt_thread.start()
    timeout = 600  # 600 seconds
    mqtt_thread.join(timeout)
    if mqtt_thread.is_alive():
        mqtt_thread.join()  # Wait for the thread to terminate gracefully
    sensor_client.disconnect()
    sensor_client.loop_stop()
    main()

def remoteSensing():
    while True:
        print("--------------------")
        print("Change Parameters")
        print("1: Sampling Rate")
        print("2: Sampling Duration")
        print("3: Sensitivity")
        print("4: Start Remote Sensing")
        print("5: Back to Main Menu")
        print("--------------------")
        while True:
            try:
                value = int(input("Enter Your Option: "))
            except:
                print("Please enter a valid number from the list")
                continue
            if value<1 or value>5:
                print("Please enter a valid number from the list")
            else:
                break
        if value==1:
            try:
                smplRate = int(input("Please enter your desired sampling rate: "))
                if smplRate<200 or smplRate>5000:
                    print("Sample Rate is out of range. Please enter a value between 200 and 5000")
                    remoteSensing()
                client = mqtt.Client("Client")
                client.connect(mqttBroker)    
                smplRate = "SAMPLERATE:" + str(smplRate)
                time.sleep(1)
                client.publish("REMOTE SENSING", smplRate)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(smplRate) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing()
            except:
                print("Please enter an appropriate value for Sampling Rate - (200-50000)")
                remoteSensing()
        if value==2:
            try:
                smplDur = int(input("Please enter your desired sampling duration: "))
                if smplDur<10 or smplDur>600:
                    print("Sample Duration is out of range, please enter a value between 10 and 600")
                    remoteSensing()
                client = mqtt.Client("Client")
                client.connect(mqttBroker)         
                smplDur = "SAMPLEDURATION:" + str(smplDur)
                time.sleep(1)
                client.publish("REMOTE SENSING", smplDur)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(smplDur) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing()
            except:
                print("Please enter an appropriate value for Sampling Duration - (10-600)")
                remoteSensing()
        if value==3:
            try:
                sens = int(input("Please enter your desired sensitivity: "))
                if sens<400 or sens>600:
                    print("Sensitivity entered is out of range. Please a enter a number between 400 and 600.")
                    remoteSensing()
                client = mqtt.Client("Client")
                client.connect(mqttBroker)      
                sens = "SENSITIVITY:" + str(sens)
                client.publish("REMOTE SENSING", sens)
                time.sleep(1)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(sens) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing()
            except:
                print("Please enter an appropriate value for Sensitivity - (400-600)")
                remoteSensing()
        if value==4:
            client = mqtt.Client("Client")
            client.connect(mqttBroker)  
            client.publish("REMOTE SENSING", "START")
            time.sleep(1)
            current_time = datetime.datetime.now().time()
            print("Just published " + "START REMOTE SENSING" + " to REMOTE SENSING", "at time", str(current_time))
            checkSampl()
        else:
            main()

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")
    main()

def mqtt_client_thread(client):
    client.on_message = on_message
    client.subscribe("SENSOR")
    client.loop_forever()

def checkSensor():
    sensor_client = mqtt.Client("SensorClient")
    sensor_client.connect(mqttBroker)
    sensor_client.publish("REMOTE SENSING", "CHECK")
    current_time = datetime.datetime.now().time()
    print("Just published " + "CHECK" + " to REMOTE SENSING", "at time", str(current_time))
    mqtt_thread = threading.Thread(target=mqtt_client_thread, args=(sensor_client,))
    mqtt_thread.start()
    timeout = 10  # 10 seconds
    mqtt_thread.join(timeout)
    if mqtt_thread.is_alive():
        mqtt_thread.join()  # Wait for the thread to terminate gracefully
    sensor_client.disconnect()
    sensor_client.loop_stop()
    main()
def on_message2(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")
    main()

def mqtt_client_thread2(client):
    client.on_message = on_message2
    client.subscribe("HISTORY")
    client.loop_forever()

def getHistory():
    sensor_client = mqtt.Client("HistoryClient")
    sensor_client.connect(mqttBroker)
    sensor_client.publish("REMOTE SENSING", "HISTORY")
    current_time = datetime.datetime.now().time()
    print("Just published " + "HISTORY" + " to REMOTE SENSING", "at time", str(current_time))
    mqtt_thread = threading.Thread(target=mqtt_client_thread2, args=(sensor_client,))
    mqtt_thread.start()
    timeout = 10  # 10 seconds
    mqtt_thread.join(timeout)
    if mqtt_thread.is_alive():
        mqtt_thread.join()  # Wait for the thread to terminate gracefully
    sensor_client.disconnect()
    sensor_client.loop_stop()
    main()
    
def autonomous():
    while True:
        print("--------------------")
        print("Change Autonomous Monitoring Timing")
        print("1: 12 Hours")
        print("2: 24 Hours")
        print("3: 48 Hours")
        print("4: Back to Main Menu")
        print("--------------------")
        while True:
            try:
                value = int(input("Enter Your Option: "))
            except:
                print("Please enter a valid number from the list")
                continue
            if value<1 or value>4:
                print("Please enter a valid number from the list")
            else:
                break
        if value == 1:
            client.publish("REMOTE SENSING", "12")
            current_time = datetime.datetime.now().time()
            print("Just published " + "12 Hours" + " to REMOTE SENSING", "at time", str(current_time))
            autonomous()
        elif value == 2:
            client.publish("REMOTE SENSING", "24")
            current_time = datetime.datetime.now().time()
            print("Just published " + "24 Hours" + " to REMOTE SENSING", "at time", str(current_time))
            autonomous()
        elif value == 3:
            client.publish("REMOTE SENSING", "48")
            current_time = datetime.datetime.now().time()
            print("Just published " + "48 Hours" + " to REMOTE SENSING", "at time", str(current_time))
            autonomous()
        elif value == 4:
            main()
        else:
            main()

def main():
    print("--------------------")
    print("Main Menu")
    print("1: Remote Sensing")
    print("2: Autonomous Monitoring")
    print("3: Check Sensor Status")
    print("4: Check History")
    print("5: Exit")
    print("--------------------")
    while True:
        try:
            value = int(input("Enter Your Option: "))
        except:
            print("Please enter a valid number from the list")
            continue
        if value<1 or value>5:
            print("Please enter a valid number from the list")
        else:
            break
    if value==1:
        remoteSensing()
    if value==2:
        autonomous()
    if value==3:
        checkSensor()
    if value==4:
        getHistory()
    if value==5:
        exit()

main()