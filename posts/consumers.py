import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Post

from django.core.serializers.json import DjangoJSONEncoder


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected: ", event)
        messages = await self.get_all_messages()
        msg = json.dumps(list(messages), sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        await self.channel_layer.send(
            self.channel_name,
            {
                "type": "websocket.message",
                "text": msg,
            }
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("received: ", event)

    async def websocket_disconnect(self, event):
        print("disconnected: ", event)

    async def websocket_message(self, event):
        print("message: ", event)
        await self.send(
            {
                "type": "websocket.send",
                "text": event['text'],
            }
        )

    @database_sync_to_async
    def get_all_messages(self):
        return Post.objects.values()


class MQTTConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected: ", event)
        await self.send(text_data=event["text"])

    async def mqtt_message(self, event):
        print("received: ", event)
        self.send({
            "type": "mqtt.send",
            "text": event["text"],
        })
        await self.save_message(event["text"])

    async def websocket_disconnect(self, event):
        print("disconnected: ", event)

    @database_sync_to_async
    def save_message(self, message):
        Post(
            topic=message["topic"],
            payload=message["payload"],
            qos=message["qos"],
            host=message["host"],
            port=message["port"],
        ).save()
