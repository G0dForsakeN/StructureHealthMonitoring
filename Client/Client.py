import paho.mqtt.client as mqtt
import datetime
import threading
import time
import sys

# Sampling Rate: 200-5000, integer, default: 200
# Sensitivity: 400-600, integer, default: 500
# Sampling Duration: 10s-600s, integer, default: 300

# Initial Declaration of MQTT Broker and Client
mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Client")
client.connect(mqttBroker)

# Package for getting SCAN RATE
def on_message1(client, userdata, message, Number):
    print(f"Received message - Actual Scan Rate: {message.payload.decode()}")
    main(Number)

def mqtt_client_thread1(client, Number):
    client.on_message = lambda client, userdata, message: on_message1(client, userdata, message, Number)
    # client.on_message = on_message1(Number=Number)
    publisher = "RETURNSCANRATE" + str(Number)
    client.subscribe(publisher)
    client.loop_forever()

def checkSampl(Number):
    sensor_client = mqtt.Client("SampleClient")
    sensor_client.connect(mqttBroker)
    mqtt_thread = threading.Thread(target=mqtt_client_thread1, args=(sensor_client, Number,))
    mqtt_thread.start()
    timeout = 600  # 600 seconds
    mqtt_thread.join(timeout)
    if mqtt_thread.is_alive():
        mqtt_thread.join()  # Wait for the thread to terminate gracefully   
    sensor_client.disconnect()
    sensor_client.loop_stop()
    main(Number)

def remoteSensing(Number):
    while True:
        print("--------------------")
        print("Change Parameters")
        print("1: Sampling Rate")
        print("2: Sampling Duration")
        print("3: Sensitivity Channel 0")
        print("4: Sensitivity Channel 1")
        print("5: Start Remote Sensing")
        print("6: Back to Main Menu")
        print("--------------------")
        while True:
            try:
                value = int(input("Enter Your Option: "))
            except:
                print("Please enter a valid number from the list")
                continue
            if value<1 or value>6:
                print("Please enter a valid number from the list")
            else:
                break
        if value==1:
            try:
                smplRate = int(input("Please enter your desired sampling rate: "))
                if smplRate<200 or smplRate>5000:
                    print("Sample Rate is out of range. Please enter a value between 200 and 5000")
                    remoteSensing(Number)
                client = mqtt.Client("Client")
                client.connect(mqttBroker)    
                smplRate = "SAMPLERATE:" + str(smplRate)
                time.sleep(1)
                publisher = "REMOTE SENSING" + str(Number)
                client.publish(publisher, smplRate)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(smplRate) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing(Number)
            except:
                print("Please enter an appropriate value for Sampling Rate - (200-50000)")
                remoteSensing(Number)
        if value==2:
            try:
                smplDur = int(input("Please enter your desired sampling duration: "))
                if smplDur<10 or smplDur>600:
                    print("Sample Duration is out of range, please enter a value between 10 and 600")
                    remoteSensing(Number)
                client = mqtt.Client("Client")
                client.connect(mqttBroker)         
                smplDur = "SAMPLEDURATION:" + str(smplDur)
                time.sleep(1)
                publisher = "REMOTE SENSING" + str(Number)
                client.publish(publisher, smplDur)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(smplDur) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing(Number)
            except:
                print("Please enter an appropriate value for Sampling Duration - (10-600)")
                remoteSensing(Number)
        if value==3:
            try:
                sens = int(input("Please enter your desired sensitivity for Channel 0: "))
                if sens<400 or sens>600:
                    print("Sensitivity entered is out of range. Please a enter a number between 400 and 600.")
                    remoteSensing(Number)
                client = mqtt.Client("Client")
                client.connect(mqttBroker)      
                sens = "SENSITIVITY0:" + str(sens)
                publisher = "REMOTE SENSING" + str(Number)
                client.publish(publisher, sens)
                time.sleep(1)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(sens) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing(Number)
            except:
                print("Please enter an appropriate value for Sensitivity - (400-600)")
                remoteSensing(Number)
        if value==4:
            try:
                sens = int(input("Please enter your desired sensitivity for Channel 1: "))
                if sens<400 or sens>600:
                    print("Sensitivity entered is out of range. Please a enter a number between 400 and 600.")
                    remoteSensing(Number)
                client = mqtt.Client("Client")
                client.connect(mqttBroker)      
                sens = "SENSITIVITY1:" + str(sens)
                publisher = "REMOTE SENSING" + str(Number)
                client.publish(publisher, sens)
                time.sleep(1)
                current_time = datetime.datetime.now().time()
                print("Just published " + str(sens) + " to REMOTE SENSING", "at time", str(current_time))
                remoteSensing(Number)
            except:
                print("Please enter an appropriate value for Sensitivity - (400-600)")
                remoteSensing(Number)        
        if value==5:
            client = mqtt.Client("Client")
            client.connect(mqttBroker)  
            publisher = "REMOTE SENSING" + str(Number)
            client.publish(publisher, "START")
            time.sleep(1)
            current_time = datetime.datetime.now().time()
            print("Just published " + "START REMOTE SENSING" + " to REMOTE SENSING", "at time", str(current_time))
            checkSampl(Number)
        else:
            main(Number)

# Package for checkSensor
def on_message(client, userdata, message, Number):
    print(f"Received message: {message.payload.decode()}")
    main(Number)

def mqtt_client_thread(client, Number):
    client.on_message = lambda client, userdata, message: on_message(client, userdata, message, Number)
    # client.on_message = on_message(Number=Number)
    publisher = "SENSOR" + str(Number)
    client.subscribe(publisher)
    client.loop_forever()

def checkSensor(Number):
    sensor_client = mqtt.Client("SensorClient")
    sensor_client.connect(mqttBroker)
    publisher = "REMOTE SENSING" + str(Number)
    sensor_client.publish(publisher, "CHECK")
    current_time = datetime.datetime.now().time()
    print("Just published " + "CHECK" + " to REMOTE SENSING", "at time", str(current_time))
    mqtt_thread = threading.Thread(target=mqtt_client_thread, args=(sensor_client, Number))
    mqtt_thread.start()
    timeout = 10  # 10 seconds
    mqtt_thread.join(timeout)
    if mqtt_thread.is_alive():
        mqtt_thread.join()  # Wait for the thread to terminate gracefully
    sensor_client.disconnect()
    sensor_client.loop_stop()
    main(Number)

# Package for getHistory
def on_message2(client, userdata, message, Number):
    print(f"Received message: {message.payload.decode()}")
    main(Number)

def mqtt_client_thread2(client, Number):
    client.on_message = lambda client, userdata, message: on_message2(client, userdata, message, Number)
    # client.on_message = on_message2
    publisher = "HISTORY" + str(Number)
    client.subscribe(publisher)
    client.loop_forever()

def getHistory(Number):
    sensor_client = mqtt.Client("HistoryClient")
    sensor_client.connect(mqttBroker)
    publisher = "REMOTE SENSING" + str(Number)
    sensor_client.publish(publisher, "HISTORY")
    current_time = datetime.datetime.now().time()
    print("Just published " + "HISTORY" + " to REMOTE SENSING", "at time", str(current_time))
    mqtt_thread = threading.Thread(target=mqtt_client_thread2, args=(sensor_client, Number))
    mqtt_thread.start()
    timeout = 10  # 10 seconds
    mqtt_thread.join(timeout)
    if mqtt_thread.is_alive():
        mqtt_thread.join()  # Wait for the thread to terminate gracefully
    sensor_client.disconnect()
    sensor_client.loop_stop()
    main(Number)
    
def autonomous(Number):
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
            publisher = "REMOTE SENSING" + str(Number)
            client.publish(publisher, "12")
            current_time = datetime.datetime.now().time()
            print("Just published " + "12 Hours" + " to REMOTE SENSING", "at time", str(current_time))
            autonomous(Number)
        elif value == 2:
            publisher = "REMOTE SENSING" + str(Number)
            client.publish(publisher, "24")
            current_time = datetime.datetime.now().time()
            print("Just published " + "24 Hours" + " to REMOTE SENSING", "at time", str(current_time))
            autonomous(Number)
        elif value == 3:
            publisher = "REMOTE SENSING" + str(Number)
            client.publish(publisher, "48")
            current_time = datetime.datetime.now().time()
            print("Just published " + "48 Hours" + " to REMOTE SENSING", "at time", str(current_time))
            autonomous(Number)
        else:
            main(Number)

def all_rpi():
    print("--------------------")
    print("Synchronize Remote Sensing/Autonomous Sensing")
    print("1: Autonomous Sensing")
    print("2: Remote Sensing")
    print("3: Main Menu")
    while True:
        try:
            value = int(input("Enter Your Option: "))
        except:
            print("Please enter a valid number from the list")
            continue
        if value<1 or value>3:
            print("Please enter a valid number from the list")
        else:
            break
    if value==1:
        client = mqtt.Client("Client")
        client.connect(mqttBroker)  
        for i in range(1,6):
            publisher = "REMOTE SENSING" + str(i)
            client.publish(publisher, "RESETAUTO")
            current_time = datetime.datetime.now().time()
            print("Just published " + "RESETAUTO" + " to REMOTE SENSING" + str(i), "at time", str(current_time))
        main_menu()
    elif value==2:
        client = mqtt.Client("Client")
        client.connect(mqttBroker)  
        for i in range(1,6):
            publisher = "REMOTE SENSING" + str(i)
            client.publish(publisher, "RESETREMOTE")
            current_time = datetime.datetime.now().time()
            print("Just published " + "RESETREMOTE" + " to REMOTE SENSING" + str(i), "at time", str(current_time))
        main_menu()
    else:
        main_menu()

def main(Number):
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
        remoteSensing(Number)
    if value==2:
        autonomous(Number)
    if value==3:
        checkSensor(Number)
    if value==4:
        getHistory(Number)
    if value==5:
        main_menu()

def main_menu():
    print("--------------------")
    print("Please choose RPI Number: ")
    print("1: RPI Number 1")
    print("2: RPI Number 2")
    print("3: RPI Number 3")
    print("4: RPI Number 4")
    print("5: RPI Number 5")
    print("6: All RPI Commands")
    print("7: Exit Code")
    print("--------------------")
    while True:
        try:
            value = int(input("Enter Your Option: "))
        except:
            print("Please enter a valid number from the list")
            continue
        if value<1 or value>7:
            print("Please enter a valid number from the list")
        else:
            break
    if value==1:
        main(1)
    if value==2:
        main(2)
    if value==3:
        main(3)
    if value==4:
        main(4)
    if value==5:
        main(5)
    if value==6:
        all_rpi()
    else: 
        sys.exit()

main_menu()