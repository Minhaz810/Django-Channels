#topic - chatapp with static group name

from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from.models import Group,Chat
import json


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("Websocket Connected...")
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name
            ,self.channel_name
            )
        self.send(
            {
                'type':'websocket.accept'
            }
        )
    
    def websocket_receive(self,event):
        print("Message Receive From Client...",event['text'])
        data = json.loads(event['text'])
        group = Group.objects.get(name = self.group_name)
        Chat.objects.create(content = data['message'],group = group)
    
        async_to_sync(self.channel_layer.group_send)(self.group_name,{
            'type':'chat.message',
            'message':event['text']
        })
       
    def chat_message(self,event):
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
    
    
    def websocket_disconnect(self,event):
        print("Channel Layer...",self.channel_layer)
        print("Channel Name",self.channel_name)
        async_to_sync(self.channel_layer.group_discard)("Friends",self.channel_name)
        print("Websocket Disconnected...")