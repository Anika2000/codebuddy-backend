# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import CollaborationSession
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        
        self.room_id = None
        await self.accept()
        self.channel_layer = get_channel_layer()
        self.group_name = 'your_group_name'  # Replace 'your_group_name' with your actual group name

        
        # Add the client to a group representing the collaborative session

        # await async_to_sync(self.channel_layer.group_add)(
        #     'your_group_name',  # Replace 'your_group_name' with your actual group name
        #     self.channel_name
        # )

        await self.channel_layer.group_add(
            self.group_name,  # Replace 'your_group_name' with your actual group name
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Hello, world!'
        }))

    async def disconnect(self, close_code):
        # Disconnect from the WebSocket
        if self.room_id:
            await self.channel_layer.group_discard(self.room_id, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        text_data_json = json.loads(text_data)
        print("hello")
        message_type = text_data_json.get('type')
        print(message_type)


        if message_type == 'create_collaboration':
            print("create collaboration is established on server")
            user_id = text_data_json.get('userId')
            room_id = text_data_json.get('roomId')
            collaboration_session, created = await database_sync_to_async(
    CollaborationSession.objects.get_or_create
)(
    room_id=room_id,
    defaults={'created_by': user_id}
)
            self.room_id = room_id
            await self.channel_layer.group_add(self.room_id, self.channel_name)
            await self.send(text_data=json.dumps({
                'type': 'created collab and in database',
                'roomId': room_id
            }))

        if message_type == 'join_collaboration':
            print("join collaboration is established on server")
            room_id = text_data_json.get('roomId')
            exists = await database_sync_to_async(CollaborationSession.objects.filter(room_id=room_id).exists)()
            if exists:
                self.room_id = room_id
                await self.channel_layer.group_add(self.room_id, self.channel_name)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Collaboration session does not exist'
                }))

        if message_type == 'code_change':
            print("code change happened")
            if self.room_id:
                print("do i get here ever?")
                code = text_data_json.get('code')
                print(f'Message received: {code}')

                await get_channel_layer().group_send(
                    self.room_id,  # Replace 'your_group_name' with your actual group name
                    {
                        'type': 'send_code_change',
                        'code': code,
                    }  
                )


    async def send_code_change(self, event):
        # Handler for broadcasting code changes to clients in the group
        code = event['code']

        # Send the code change message to the client
        
        await self.send(text_data=json.dumps({
            'type': 'code_change',
            'code': code,
        })) 
        
