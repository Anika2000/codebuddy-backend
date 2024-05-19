# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        

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
        await self.close()

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        text_data_json = json.loads(text_data)
        print("hello")
        message_type = text_data_json.get('type')
        print(message_type)
        if message_type == 'code_change':
            code = text_data_json.get('code')
            print(f'Message received: {code}')

            await get_channel_layer().group_send(
                self.group_name,  # Replace 'your_group_name' with your actual group name
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
        
