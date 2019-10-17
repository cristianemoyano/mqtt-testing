import click
import random
import time
import logging
from client import MQTTClient

logger = logging.getLogger(__name__)


def get_topic_message():
    element = 'home'
    areas = ['front', 'back', 'kitchen', 'basement', 'living']
    entrances = ['door', 'window']
    states = ['true', 'false']
    area = random.choice(areas)
    if (area in ['basement', 'living']):
        topic = element + '/' + area + '/temp'
        logger.info(topic)
        message = random.randrange(0, 30, 1)
        logger.info(message)
    else:
        topic = element + '/' + area + '/' + random.choice(entrances)
        logger.info(topic)
        message = random.choice(states)
        logger.info(message)
    return topic, message


@click.command()
@click.option('--client_id', default=None, help='MQTT Client Id')
@click.option('--topic', default='test', help='MQTT Topic that the message should be published on')
@click.option('--msg', default='my message', help='MQTT Message to publish')
@click.option('--qos', default=0, help='The quality of service level to use for the will.')
@click.option(
    '--retain',
    default=False,
    help=(
        'if set to True, the message will be set as the “last known good”/retained message for the topic.'
    ),
)
@click.option('--log', default=None, help='Enable log')
@click.option('--ws', default=None, help='Enable Websocket URL')
@click.option('--auto', default=None, help='Auto generate topic/message')
@click.option('--loop', default=None, help='Loop topic/message')
def run(client_id, topic, msg, qos, retain, log, ws, auto, loop):

    logging.basicConfig(
        level={
            0: logging.WARN,
            1: logging.INFO,
        }.get(log, logging.DEBUG),
        format="%(asctime)-15s %(levelname)-8s %(message)s",
    )

    mqtt_client = MQTTClient(
        client_id=client_id,
        enable_log=log,
        enable_ws=ws,
    ).connect()

    if auto and not loop:
        auto_topic, auto_msg = get_topic_message()
        # Publish a message
        mqtt_client.publish(
            topic=auto_topic,
            payload=auto_msg,
            qos=qos,
            retain=retain,
        )
    elif auto and loop:
        while True:
            auto_topic, auto_msg = get_topic_message()
            # Publish a message
            mqtt_client.publish(
                topic=auto_topic,
                payload=auto_msg,
                qos=qos,
                retain=retain,
            )
            time.sleep(5)
    else:
        # Publish a message
        mqtt_client.publish(
            topic=topic,
            payload=msg,
            qos=qos,
            retain=retain,
        )


if __name__ == '__main__':
    # python test_publish.py --client_id arduino --msg hello --topic test
    run()
