
from django.db.models import fields
from rest_framework import serializers
from datetime import datetime


from .models import Order,Order_detail,OrderMercadoPagoDetail,AnonymousPersonalData
from apps.orders import models
from apps.products.models import Product
from apps.tiendas.models import Tienda,Envios

from apps.users.models import User,UserPersonalData

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = (
            'id',
            'name',
            'title',
        )


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class UserDataSerializer(serializers.ModelSerializer):

    user = UserDataSerializer()

    class Meta:
        model = UserPersonalData
        fields = ('__all__')

class AnonymousUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousPersonalData
        fields = ('__all__')

class EnviosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envios
        fields =('__all__')


class OrderSerializer(serializers.ModelSerializer):

    productos = serializers.SerializerMethodField()
    tienda= TiendaSerializer()
    personal_user_data = UserDataSerializer()
    anonymous_user_data = AnonymousUserDataSerializer()
    envio=EnviosSerializer()

    class Meta:
        model = Order
        fields = (
            'tienda',
            'created',
            'id',
            'user',        
            'notas' ,
            'total' ,
            'estado' ,
            'metodo_pago' ,
            'quantity_products',
            'productos',
            'personal_user_data',
            'visto',
            'mercado_pago_approved',
            'pago',
            'anonymous_user_data',
            'envio',
        )

    def get_productos(self,obj):
        query = Order_detail.objects.productos_por_ventas(obj.id)
        productos_serializados = OrderProductDetailSerializer(query,many=True).data
        return productos_serializados

class ProductInOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=(
            'id',
            'title',
            'image',
        )

class OrderProductDetailSerializer(serializers.ModelSerializer):
    product = ProductInOrderDetailSerializer()
    class Meta:
        model = Order_detail
        fields = ('__all__')


class ProductDetailSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    variacion_id = serializers.IntegerField(required=False)
    opciones = serializers.ListField(required=False)


class ProcesoOrderSerializer(serializers.Serializer):
    
    tienda = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10,decimal_places=2)
    metodo_pago = serializers.CharField()
    quantity_products = serializers.IntegerField(min_value=1)
    productos = ProductDetailSerializer(many=True)
    personal_user_data = serializers.IntegerField()
    envio = serializers.CharField(required=False,allow_null=True)

class ProcesoOrderAnonymousSerializer(serializers.Serializer):
    
    tienda = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10,decimal_places=2)
    metodo_pago = serializers.CharField()
    quantity_products = serializers.IntegerField(min_value=1)
    productos = ProductDetailSerializer(many=True)
    anonymous_user_data = serializers.IntegerField()
    envio = serializers.CharField(required=False,allow_null=True)


class ProductDetailToCancelSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    variacion_id = serializers.IntegerField(required=False, allow_null=True)


class CancelarOrdenSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    productos = ProductDetailToCancelSerializer(many=True)


class OrderEstadoSereializer(serializers.ModelSerializer):
    
    class Meta:
       model = Order
       fields = ('estado',)

class OrderPagoEstadoSereializer(serializers.ModelSerializer):
    
    class Meta:
       model = Order
       fields = ('pago',)


class OrderVistoSerializer(serializers.Serializer):

    order_id = serializers.IntegerField()


class MercadoPagoSerializer(serializers.Serializer):
    
    tienda_id = serializers.IntegerField()
    tienda= serializers.CharField()
    total = serializers.DecimalField(max_digits=10,decimal_places=2)
    orden = serializers.IntegerField()


class MercadoPagoDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderMercadoPagoDetail
        fields = ('__all__')

class OrderUpdataMetodoPagoStatus(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields= ('mercado_pago_approved',)

class ClearOrdersNoVistasSerializer(serializers.Serializer):
    tienda_id = serializers.IntegerField()
    

class OnlyTiendaIdSerializer(serializers.Serializer):

    tienda = serializers.IntegerField()


