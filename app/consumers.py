import random

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class StudentConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("student", self.channel_name)
        self.scope["session"]["seed"] = random.randint(1, 1000)
        self.scope["session"].save()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("student",
                                                        self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            print(text_data)

    def join_class(self, event):
        self.send(text_data=event["text"])


class ProfessorConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.scope["session"]["seed"] = random.randint(1, 1000)
        self.scope["session"]["class_code"] = random.randint(1, 1000)
        async_to_sync(self.channel_layer.group_add)(
            "professor-" + self.scope["session"]["class_code"],
            self.channel_name)
        self.scope["session"].save()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "professor-" + self.scope["session"]["class_code"],
            self.channel_name)
