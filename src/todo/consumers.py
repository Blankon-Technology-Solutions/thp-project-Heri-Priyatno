from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.text import slugify


class TodoConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = f"todo_{slugify(self.user.email)}"
        #
        # # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def todo_update(self, event):
        self.send(text_data="Updated")
