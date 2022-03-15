# from django.contrib.auth import get_user_model
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json
# from .models import Message, User
# from django.shortcuts import render, get_object_or_404

# User = get_user_model()


# class ChatConsumer(WebsocketConsumer):

#     def fetch_messages(self, data):
#         pass
#     #     messages = Message.objects.filter(chat_room=1)[:10]
#     #     content = {
#     #         'command': 'messages',
#     #         'messages': self.messages_to_json(messages)
#     #     }
#     #     self.send_chat_message(content)

#     def new_message(self, data):
#         send_by_user = get_object_or_404(User, username=data['from'])
#         send_to_user = get_object_or_404(User, username=data['to'])
#         message = Message.objects.create(
#             chat_room=chat_room,
#             created_by=send_by_user,
#             send_to=send_to_user,
#             content=data['message'])

#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         return self.send_chat_message(content)

#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result

#     def message_to_json(self, message):
#         return {
#             'id': message.id,
#             'author': message.created_by.username,
#             'content': message.content,
#             'created_date': str(message.created_date)
#         }

#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }

#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)

#     def send_chat_message(self, message):
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     def send_message(self, message):
#         print(message)
#         self.send(text_data=json.dumps({
#                 message
#             })
#         )

#     def chat_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps(message))