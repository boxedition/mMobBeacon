# Requiment:
# pip install paho-mqtt keyboard
import paho.mqtt.client as mqtt
import os
from datetime import datetime
import threading

# MQTT configuration
MQTT_SERVER = "192.168.221.44"
MQTT_USER = "mqtt"
MQTT_PASSWORD = "mqtt"
MQTT_TOPIC = "ble"
CLIENT_ID = "MQTTPython"

# Log file
LOG_FILE = "logs.txt"

# Connect to MQTT server
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_SERVER, 1883, 60)

# Callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Timestamp with milliseconds
    message = msg.payload.decode().strip()
    print(f"Received message: {timestamp} - {message}")
    with open(LOG_FILE, "a") as f:
        f.write(f"{message},{timestamp}\n")

# Register MQTT callback functions
client.on_connect = on_connect
client.on_message = on_message

# Start MQTT loop in a separate thread
client.loop_start()

# Function to handle disconnection and file renaming
def handle_disconnection():
    client.disconnect()
    new_file_name = input("Enter a new name for the log file: ")
    if new_file_name.strip() != "":
        os.rename(LOG_FILE, new_file_name.strip() + ".txt")

# Timer function to disconnect after 15 seconds
def disconnect_after_15_seconds():
    threading.Timer(10.0, handle_disconnection).start()

# Start the timer
disconnect_after_15_seconds()

# Wait for the timer to finish
threading.Event().wait()

# Stop the MQTT loop and disconnect
client.loop_stop()
client.disconnect()
