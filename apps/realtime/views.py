import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.

class test(APIView):
    
    
    def get(self,request):
        res = {
            'tienda_id': 'tienda_id'
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifi',{
                'type' : 'send_notifi',
                'text' : json.dumps(res)
            }
        ) 
        

        return Response({'msj':'ok'},status=status.HTTP_200_OK)
