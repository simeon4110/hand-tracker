import random

from channels.generic.websocket import WebsocketConsumer


class StudentConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.scope["session"]["seed"] = random.randint(1, 1000)
        self.scope["session"].save()


class ProfessorConsumer(WebsocketConsumer):
    def connect(self):
        self.scope["session"]["seed"] = random.randint(1, 1000)
        self.scope["session"].save()
