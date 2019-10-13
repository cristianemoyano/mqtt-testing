import click
from client import MQTTClient


@click.command()
@click.option('--client_id', default=None, help='MQTT Client Id')
@click.option('--topic', default='test', help='MQTT Topic to publish')
@click.option('--msg', default='my message', help='MQTT Message to publish')
@click.option('--log', default=None, help='Enable log')
def run(client_id, topic, msg, log):

    mqtt_client = MQTTClient(
        client_id=client_id,
        enable_log=log,
    ).get_mqtt_client()
    # Publish a message
    mqtt_client.publish(topic, msg)


if __name__ == '__main__':
    # python test_publish.py --client_id arduino --msg hello --topic test
    run()
