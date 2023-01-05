# https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import os
import requests

broker_name = os.environ["MQTT_BROKER_NAME"]
broker_port = os.environ["MQTT_BROKER_PORT"]
broker_channel = os.environ["MQTT_BROKER_CHANNEL"]
robot_api_endpoint = os.environ["ROBOT_API_ENDPOINT"]

# MQTT gateway for automatic run submittion

# Translates mqtt messages from a broker in a certain channel into REST requests of robot_api_endpoint



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(broker_channel)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if topic != broker_channel:
        return
    res = requests.post(robot_api_endpoint,data=msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_name, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
