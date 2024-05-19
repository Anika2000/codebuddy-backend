# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

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
        
