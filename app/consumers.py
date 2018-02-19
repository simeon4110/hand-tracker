import random
import json
from channels.generic.websocket import SyncConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class JoinClass(SyncConsumer):
    class_number = None
    student_name = None

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        json_data = json.loads(event["text"])
        if json_data["student_name"]:
            self.student_name = str(json_data["student_name"])
            self.class_number = str(json_data["class_number"])

        else:
            self.student_name = "ERROR"
            self.class_number = "ERROR"

        self.send({
            "type": "websocket.send",
            "text": self.class_number,
        })

    def websocket_disconnect(self, event):
        self.send({
            "type": "websocket.disconnect"
        })

    def websocket_send(self, event):
        if event["class-number"]:
            return self.class_number
