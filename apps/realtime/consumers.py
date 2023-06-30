from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json



class WSConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """ self.accept()
        self.send(json.dumps({'message':'Connected'})) """

        await self.channel_layer.group_add('notifi',self.channel_name)
        await self.accept()
        self.send(text_data=json.dumps({'msj':'connected'}))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('notifi',self.channel_name)

    async def send_notifi(self,event):
        data = json.loads(event['text'])

        await self.send(text_data=json.dumps({'newOrder':data}))

    async def send_notifi_booking(self,event):
        data = json.loads(event['text'])

        await self.send(text_data=json.dumps({'newBooking':data}))

    async def send_notifi_question(self,event):
        data = json.loads(event['text'])

        await self.send(text_data=json.dumps({'newQuestion':data}))

    async def send_notifi_question_service(self,event):
        data = json.loads(event['text'])

        await self.send(text_data=json.dumps({'newQuestion_service':data}))
        



    

            