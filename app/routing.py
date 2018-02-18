from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from app.consumers import *

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("^student-socket/$", StudentConsumer, name="student"),
            url("^professor-socket/$", ProfessorConsumer, name="professor")
        ])
    ),
})
