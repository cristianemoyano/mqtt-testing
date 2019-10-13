import click
from client import MQTTClient


@click.command()
@click.option('--client_id', default=None, help='MQTT Client Id')
@click.option('--topic', default='test', help='Single MQTT Topic to subscribe')
@click.option('--topics', default=None, help='List of MQTT Topic separated by comma to subscribe')
@click.option('--qos', default=0, help='The quality of service level to use for the will.')
@click.option('--log', default=None, help='Enable log')
def run(client_id, topic, topics, qos, log):

    mqtt_client = MQTTClient(
        client_id=client_id,
        enable_log=log,
    ).get_mqtt_client()

    if topics:
        # Topics by comma
        for topic in [x.strip() for x in topics.split(',')]:
            mqtt_client.subscribe(topic, qos)  # Once the client has connected to the broker, subscribe to the topic
    else:
        mqtt_client.subscribe(topic, qos)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = mqtt_client.loop_forever()
    print("rc: " + str(rc))


if __name__ == '__main__':
    # python server.py --client_id server --topic test
    run()
