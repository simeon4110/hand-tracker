from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from app.consumers import *

application = ProtocolTypeRouter({

    "websocket": SessionMiddlewareStack(
        URLRouter([
            url("^student-socket/$", StudentConsumer, name="student"),
            url("^professor-socket/$", ProfessorConsumer, name="professor")
        ])
    ),
})
