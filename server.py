import paho.mqtt.client as mqtt
import os
from urllib.parse import urlparse


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


mqttc_client = mqtt.Client()
# Assign event callbacks
mqttc_client.on_message = on_message
mqttc_client.on_connect = on_connect

# Uncomment to enable debug messages
# mqttc_client.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://mosquitto:mosquitto@localhost:1883')
url = urlparse(url_str)
topic = url.path[1:] or 'test'

# Connect
mqttc_client.username_pw_set(url.username, url.password)
mqttc_client.connect(url.hostname, url.port)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc_client.loop_forever()
