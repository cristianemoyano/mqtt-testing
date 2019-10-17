import logging
import time
import signal

from asgiref.sync import async_to_sync

from mqtt_client import MQTTClient
# import paho.mqtt.client as mqtt


logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with status {}".format(rc))
    client.subscribe("#", 2)


def on_disconnect(client, userdata, rc):
    server = userdata["server"]
    logger.info("Disconnected")
    if not server.stop:
        j = 3
        for i in range(j):
            logger.info("Trying to reconnect")
            try:
                client.reconnect()
                logger.info("Reconnected")
                break
            except Exception as e:
                if i < j:
                    logger.warn(e)
                    time.sleep(1)
                    continue
                else:
                    raise


def on_message(client, userdata, message):
    logger.debug("Received message from topic {}".format(message.topic))
    channel = userdata["channel"]
    msg = {
        "topic": message.topic,
        "payload": message.payload,
        "qos": message.qos,
        "host": userdata["host"],
        "port": userdata["port"],
    }
    try:
        async_to_sync(channel.application_mapping['mqtt'].save_message)(msg)
    except Exception as e:
        logger.error("Cannot send message {}".format(msg))
        logger.exception(e)


class Server(object):
    def __init__(self, channel, host, port, username=None, password=None):
        self.channel = channel
        self.host = host
        self.port = port
        self.client = MQTTClient(
            userdata={
                "server": self,
                "channel": self.channel,
                "host": self.host,
                "port": self.port,
            },
            callbacks={
                'on_connect': on_connect,
                'on_disconnect': on_disconnect,
                'on_message': on_message,
            }
        ).connect()

    def stop_server(self, signum, frame):
        logger.info("Received signal {}, terminating".format(signum))
        self.stop = True

    def set_signal_handlers(self):
        signal.signal(signal.SIGTERM, self.stop_server)
        signal.signal(signal.SIGINT, self.stop_server)

    def run(self):
        self.stop = False
        self.set_signal_handlers()
        logger.info("Starting loop")
        while not self.stop:
            logger.debug("Restarting loop")
            self.client.loop()

        self.client.disconnect()
