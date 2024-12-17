import binascii
import datetime
import socket
import urllib
from urllib.request import urlopen
import time
import paho.mqtt.client as mqtt
import json
import base64
from datetime import datetime
import csv
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import requests

mqtt_borker_address = "212.98.137.194"
mqtt_port = 1883
device_eui = "5cec206fca6ff601"
device_name = "Device1"
emonApiKey = "29a142d2ac623f1aa7d623ee8fa240fc"  # Remplacer par votre API code

# Fonction pour transformer une chaîne en objet JSON
def transform_to_json(message_string):

    # Split the input string by commas to separate key-value pairs

    pairs = message_string.split(", ")

    # Initialize an empty dictionary to store the key-value pairs

    json_data = {}

    # Iterate through each key-value pair

    for pair in pairs: 

        # Split the pair by ": " to extract key and value

        key, value = pair.split(":", 1)

        # Strip any leading or trailing whitespace from the key and value

        key = key.strip()

        value = value.strip()

        # Add the key-value pair to the dictionary

        json_data[key] = value

    return json_data

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("application/31/device/5cec206fca6ff601/rx")  # remplacer par votre node-id

# def on_message(client, userdata, msg):
#     print(msg.topic + " " + str(msg.payload))
#     data = json.loads(msg.payload)

#     if 'data' not in data.keys():
#         return

#     json_payload = base64.b64decode(data['data'])
    
#     print(json_payload)
    
#     # Transformer la chaîne en objet JSON
#     json_data = transform_to_json(json_payload)
    
#     # Prepare the URL 
#     # url = "http://emoncms.org/input/post.json?node=" + str("5f812483c73778fb") + "&apikey=" + emonApiKey + "&json=" + urllib2.quote(json.dumps(json_data))
#     url = "http://emoncms.org/input/post.json?node=" + str("5f812483c73778fb") + "&apikey=" + emonApiKey + "&json=" + urllib.parse.quote(json.dumps(json_data))
    
#     # Send the data to emoncms
#     try:
#         # urllib2.urlopen(url)
#         #print url
#         response = urllib.request.urlopen(url)
#         # Read the response if necessary
#         response_data = response.read()
#         print(response_data)
#     except urllib.error.URLError as e:
#         print("Error:", e)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print("Hi")
    
    # Extract 'data' field from the string
    message_str = msg.payload.decode("utf-8")
    data_start = message_str.find('"data":"') + len('"data":"')
    data_end = message_str.find('","object":')
    data_field = message_str[data_start:data_end]
    
    # Check if 'data' field is null or not present
    # if data_field == "null" or not data_field:
    #     print("No data available")
    #     # Set a default value for data_field
    #     data_field = "U3RhdGU6IE9jY3VwaWVkLCBQbGFjZTogMjMsIFBhcmtpbmc6IFdhdmVz"  # Default base64 encoded data
    if len(data_field)>150:
        print("No data available")
        return
        # Set a default value for data_field
        data_field = "U3RhdGU6IE9jY3VwaWVkLCBQbGFjZTogMjMsIFBhcmtpbmc6IFdhdmVz"  # Default base64 encoded data
    try:
        # Decode 'data' field from base64
        print("12313213123123132")
        print(data_field)
        decoded_data = base64.b64decode(data_field).decode("utf-8")
        print("89080980808080809")
    except binascii.Error as e:
        print("Error decoding base64:", e)
        print("Invalid base64-encoded string:", data_field)
        return  # Exit the function if decoding fails
    except UnicodeDecodeError as e:
        print("Error decoding base64:", e)
        print("Invalid base64-encoded data:", data_field)
        return  # Exit the function if decoding fails
    
    # Transform decoded data into JSON
    print("Heyyyyy")
    json_data = transform_to_json(decoded_data)
    print(json_data)
    
    # Prepare the URL for emoncms
    # url = "http://emoncms.org/input/post.json?node=" + str("5f812483c73778fb") + "&apikey=" + emonApiKey + "&json=" + urllib.parse.quote(json.dumps(json_data))
    # url = "http://your-node-backend.com/api/data"
    url = "http://localhost:3000/arduino-data/data"
    print("Hello")
    # Send the data to emoncms
    # try:
    #     response = urllib.request.urlopen(url)
    #     response_data = response.read()
    #     print(response_data)
    #     print("Lol")
    # except urllib.error.URLError as e:
    #     print("Error:", e)
    try:
        response = requests.post(url, json=json_data)
        response_data = response.json()
        print(response_data)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

#client = mqtt.Client(client_id="bc52dd82272149e7803f211e93ed0a3e", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp", callback_api_version=mqtt.MQTTv31)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="39b8e887a2a54d2cb60f6d8bd2d871a6")

client.username_pw_set("user", "bonjour")
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_borker_address, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()