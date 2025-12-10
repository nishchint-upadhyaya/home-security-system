import serial
import time
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env from current directory

# Ubidots config
UBIDOTS_TOKEN = os.getenv("UBIDOTS_TOKEN")
DEVICE_LABEL = "home-security"
VARIABLE_LABEL = "recludo_trigger"

MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_TOPIC = f"/v1.6/devices/{DEVICE_LABEL}"

# Serial config
SERIAL_PORT = "/dev/cu.usbmodem101"
BAUD_RATE = 115200

def on_connect(client, userdata, flags, rc):
    # print("Connected to MQTT Broker")
    print(f"Connected to MQTT Broker with result code {rc}")

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(UBIDOTS_TOKEN, "")
mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# Line below opens a serial port - equivalent to opening Serial Monitor in Arduino IDE
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
print("Listening for serial messages...")

while True:
    line = ser.readline().decode("utf-8").strip()
    if "recludo_detected" in line:
        print("Keyword detected. Sending to Ubidots...")
        payload = {
            VARIABLE_LABEL: {
                "value": 1,
                # "value": int(time.time()),  # send UNIX timestamp instead of same value over and over - time.time() gives the number of seconds since Jan 1, 1970 UTC
                "context": { "status": "success" }
            }
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print("Data sent to Ubidots!")
        
        time.sleep(2)
        break

    elif "recludo_not_detected" in line:
        print("Keyword not detected within time window. Sending to Ubidots...")
        payload = {
            VARIABLE_LABEL: {
                "value": 0,
                # "value": int(time.time()),  # send UNIX timestamp instead of same value over and over - time.time() gives the number of seconds since Jan 1, 1970 UTC
                "context": { "status": "failed" }
            }
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print("Data sent to Ubidots!")
        
        time.sleep(2)
        break