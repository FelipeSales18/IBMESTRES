import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("projects", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("projects", self.channel_name)

    async def project_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "project",
            "data": event["data"]
        }))

class TeamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("teams", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("teams", self.channel_name)

    async def team_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "team",
            "data": event["data"]
        }))