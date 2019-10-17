import paho.mqtt.client as mqtt
import os
import logging
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected!", str(rc))  # rc is the error code returned when connecting to the broker


def on_message(client, obj, msg):
    logger.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(client, obj, mid):
    logger.info("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    log = "{c} {obj} {level} {str}".format(c=client, obj=obj, level=level, str=string)
    logger.info(log)


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
            enable_ws=False,
            callbacks=None,
            userdata=None,
        ):
            self.client_id = client_id
            self.enable_log = enable_log
            self.enable_ws = enable_ws
            self.callbacks = callbacks if callbacks else MQTT_DEFAULT_CALLBACKS
            self.client = mqtt.Client(
                userdata=userdata,
                client_id=self.client_id if self.client_id else "",
                clean_session=False if self.client_id else True,
                protocol=mqtt.MQTTv311,
            )

        def connect(self):
            # Assign event callbacks
            for key, callback in self.callbacks.items():
                setattr(self.client, key, callback)

            # Uncomment to enable debug messages
            if self.enable_log:
                self.client.on_log = on_log

            # Parse CLOUDMQTT_URL (or fallback to localhost)
            env = 'CLOUDMQTT_URL_WS' if self.enable_ws else 'CLOUDMQTT_URL'
            url_str = os.getenv(env)
            url = urlparse(url_str)

            # Connect
            if not self.enable_ws:
                self.client.username_pw_set(url.username, url.password)
            self.client.connect(
                host=url.hostname,
                port=url.port,
                keepalive=60,
                bind_address="",
            )

        def __str__(self):
            return repr(self) + self.client_id

    instance = None

    def __init__(
            self,
            client_id=None,
            enable_log=False,
            enable_ws=False,
            callbacks=None,
            userdata=None,
    ):
        if not MQTTClient.instance:
            MQTTClient.instance = MQTTClient.__MQTTClient(
                client_id=client_id,
                enable_log=enable_log,
                enable_ws=enable_ws,
                callbacks=callbacks,
                userdata=userdata,
            )
        else:
            MQTTClient.instance.client_id = client_id
            MQTTClient.instance.enable_log = enable_log
            MQTTClient.instance.enable_ws = enable_ws
            MQTTClient.instance.callbacks = callbacks
            MQTTClient.instance.userdata = userdata

    def connect(self):
        self.instance.connect()
        return getattr(self.instance, 'client')

    def __getattr__(self, name):
        return getattr(self.instance, name)
