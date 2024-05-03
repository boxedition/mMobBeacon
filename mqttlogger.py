# Requiment:
# pip install paho-mqtt keyboard
import paho.mqtt.client as mqtt
import keyboard
import os
from datetime import datetime

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

# Keyboard shortcuts
def on_ctrl_a(event=None):
    with open(LOG_FILE, "a") as f:
        f.write("##OPEN\n")

def on_ctrl_d(event=None):
    with open(LOG_FILE, "a") as f:
        f.write("##CLOSED\n")


# Register keyboard shortcuts
keyboard.add_hotkey('ctrl+a', on_ctrl_a)
keyboard.add_hotkey('ctrl+d', on_ctrl_d)

# Function to handle keyboard interrupts (Ctrl+C)
def handle_keyboard_interrupt():
    client.disconnect()
    new_file_name = input("Enter a new name for the log file: ")
    if new_file_name.strip() != "":
        os.rename(LOG_FILE, new_file_name.strip() + ".txt")

# Wait for keyboard interrupts (Ctrl+C)
try:
    keyboard.wait()
except KeyboardInterrupt:
    handle_keyboard_interrupt()

# Disconnect MQTT client and stop the loop
client.loop_stop()
client.disconnect()
