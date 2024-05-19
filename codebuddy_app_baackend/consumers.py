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
        pass
