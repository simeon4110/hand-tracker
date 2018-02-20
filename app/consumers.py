"""
The async WebSockets -- Currently only a single Json consumer.
"""
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from app.models import ClassRoom
from app.models import Student


class ClassConsumer(AsyncJsonWebsocketConsumer):
    rooms = None

    async def connect(self):
        """
        Accepts all incoming connections, because why not?
        :return: Nothing
        """
        await self.accept()
        self.rooms = set()

    async def receive_json(self, content, **kwargs):
        """
        Deals with all incoming hits to the WebSocket. Routes traffic via
        command definitions.
        :return: Nothing.
        """
        command = content.get("command", None)
        class_id = content.get("class_id", None)
        user_name = content.get("student_name", None)

        if command == "join-prof":
            await self.join_class(class_id, user_name)

        if command == "clear-hands":
            await self.clear_hands(class_id)

        if command == "join":
            await self.join_class(class_id, user_name)

        if command == "leave":
            await self.leave_class(class_id, user_name)

        if command == "raise":
            await self.set_hand(class_id, user_name, True)

        if command == "lower":
            await self.set_hand(class_id, user_name, False)

    @staticmethod
    async def clear_hands(class_id):
        """
        Clears all the hands raised in a ClassRoom.
        :param class_id: The ClassRoom to clear.
        :return: Nothing.
        """
        try:
            room = ClassRoom.objects.get(class_number=class_id)
        except Exception as e:
            print(e)
            return None

        student_list = Student.objects.filter(class_room=room.id)

        for student in student_list:
            student.hand = False
            student.save()

    async def set_hand(self, class_id, user_name, hand):
        """
        Set's a student's hand to raised (true) or not (false).
        :param class_id: The class the student is in.
        :param user_name: The student's name.
        :param hand: Boolean true = raised.
        :return: Initiates event to reset list of raised hands.
        """
        try:
            room = ClassRoom.objects.get(class_number=class_id)
            student = Student.objects.get(student_name=user_name)
        except Exception as e:
            print(e)
            return None

        student.hand = hand
        student.save()

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "hand.change",
                "class_id": class_id,
                "username": user_name,
            }
        )

    async def join_class(self, class_id, user_name):
        """
        Joins a specific class channel.
        :param class_id: The class to join.
        :param user_name: The user's user_name.
        :return: Initiates an join event, broadcasting to all room members.
        """
        try:
            room = ClassRoom.objects.get(class_number=class_id)
        except Exception as e:
            print(e)
            return None

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "room.join",
                "class_id": room.group_name,
                "username": user_name,
            }
        )

        self.rooms.add(room.id)  # This is needed for proper socket closing.

        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name
        )

        await self.send_json({
            "join": str(room.id),
            "title": room.group_name,
        })

    async def leave_class(self, class_id, user_name):
        """
        :TODO: Fix this!!!!
        :param class_id: The class to leave.
        :param user_name: The person leaving.
        :return: An event notifying the room a user has left.
        """

        room = ClassRoom.objects.get(pk=class_id)

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "room.leave",
                "class_id": class_id,
                "user_name": user_name,
            }
        )

        self.rooms.discard(class_id)

        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name
        )

        await self.send_json({
            "leave": room.id
        })

    async def disconnect(self, code):
        for room in self.rooms:
            await self.leave_class(room, "")

    # HELPER METHODS -- Handle the message dispatching. And object manipulation.

    async def room_join(self, event):
        await self.send_json(
            {
                "msg_type": 0,
                "room": event["class_id"],
                "username": event["username"],
            }
        )

    async def room_leave(self, event):
        await self.send_json(
            {
                "msg_type": 0,
                "room": event["class_id"],
                "username": event["username"],
            }
        )

    async def hand_change(self, event):
        class_room = ClassRoom.objects.get(class_number=event["class_id"])
        hand_list = {}

        for student in Student.objects.filter(
                class_room=class_room.id).values_list("hand", "student_name",
                                                      "modifier"):
            if student[0]:
                hand_list[student[1]] = student[2]

        await self.send_json(
            {
                "msg_type": 2,
                "room": event["class_id"],
                "user_list": hand_list,
            }
        )
