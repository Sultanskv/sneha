from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LeadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # await self.channel_layer.group_add("leads_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("leads_group", self.channel_name)

    async def notify(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
        }))


# class LeadConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def send_new_lead(self, event):
#         lead_name = event['lead_name']
#         await self.send(text_data=json.dumps({
#             'lead_name': lead_name
#         }))