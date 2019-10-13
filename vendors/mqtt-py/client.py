import paho.mqtt.client as mqtt
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()


def on_connect(client, userdata, flags, rc):
    print("Connected!", str(rc))  # rc is the error code returned when connecting to the broker


def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    log = "{c} {obj} {level} {str}".format(c=client, obj=obj, level=level, str=string)
    print(log)


MQTT_DEFAULT_CALLBACKS = {
    'on_connect': on_connect,
    'on_message': on_message,
    'on_publish': on_publish,
    'on_subscribe': on_subscribe,
}


class MQTTClient(object):
    """
    Singleton MQTT Client
    """
    class __MQTTClient:
        def __init__(
            self,
            client_id=None,
            enable_log=False,
            callbacks=None,
        ):
            self.client_id = client_id
            self.enable_log = enable_log
            self.callbacks = callbacks if callbacks else MQTT_DEFAULT_CALLBACKS

        def connect(self):
            mqtt_client = mqtt.Client(
                client_id=self.client_id if self.client_id else "",
                clean_session=False if self.client_id else True,
            )
            # Assign event callbacks
            for key, callback in self.callbacks.items():
                setattr(mqtt_client, key, callback)

            # Uncomment to enable debug messages
            if self.enable_log:
                mqtt_client.on_log = on_log

            # Parse CLOUDMQTT_URL (or fallback to localhost)
            url_str = os.getenv('CLOUDMQTT_URL')
            url = urlparse(url_str)

            # Connect
            mqtt_client.username_pw_set(url.username, url.password)
            mqtt_client.connect(
                host=url.hostname,
                port=url.port,
                keepalive=60,
                bind_address="",
            )
            self.mqtt_client = mqtt_client

        def __str__(self):
            return repr(self) + self.client_id

    instance = None

    def __init__(
            self,
            client_id=None,
            enable_log=False,
            callbacks=None,
    ):
        if not MQTTClient.instance:
            MQTTClient.instance = MQTTClient.__MQTTClient(
                client_id=client_id,
                enable_log=enable_log,
                callbacks=callbacks,
            )
        else:
            MQTTClient.instance.client_id = client_id
            MQTTClient.instance.enable_log = enable_log
            MQTTClient.instance.callbacks = callbacks

        MQTTClient.instance.connect()

    def get_mqtt_client(self):
        return getattr(self.instance, 'mqtt_client')

    def __getattr__(self, name):
        return getattr(self.instance, name)
