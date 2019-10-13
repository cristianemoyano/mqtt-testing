import click
from client import MQTTClient


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
def run(client_id, topic, msg, qos, retain, log):

    mqtt_client = MQTTClient(
        client_id=client_id,
        enable_log=log,
    ).get_mqtt_client()
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
