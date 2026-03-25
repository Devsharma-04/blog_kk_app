import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message, Thread

# 1. Notification Consumer (Iska naam exact yahi hona chahiye)
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        if self.user and self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event.get("value", {})))

# 2. Chat Consumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        # URL parameters safely get karna
        url_route = self.scope.get('url_route', {})
        self.other_user_id = url_route.get('kwargs', {}).get('id')

        if self.user and self.user.is_authenticated and self.other_user_id:
            self.my_id = self.user.id
            ids = sorted([int(self.my_id), int(self.other_user_id)])
            self.room_name = f'chat_{ids[0]}_{ids[1]}'

            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # receive method fixed (method overrides base class correctly)
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)
            message = data.get('message', '')
            
            await self.save_message(message)

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.my_id
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id']
        }))

    @database_sync_to_async
    def save_message(self, message):
        try:
            other_user = User.objects.get(id=self.other_user_id)
            u1, u2 = (self.user, other_user) if self.user.id < other_user.id else (other_user, self.user)
            thread_obj, _ = Thread.objects.get_or_create(first_person=u1, second_person=u2)
            
            Message.objects.create(
                thread=thread_obj,
                sender=self.user,
                receiver=other_user,
                content=message
            )
        except Exception as e:
            print(f"Error saving message: {e}")