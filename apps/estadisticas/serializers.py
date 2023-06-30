from rest_framework import serializers
from django.db.models import Count, Avg

from apps.users.models import (
    UserPersonalData,
    User
)
from apps.products.models import (
    Product
    )
from apps.orders.models import (
    Order,
    Order_detail,
    AnonymousPersonalData
)

class GenericStaticsSerializer(serializers.Serializer):
    product = serializers.CharField()

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalData
        fields = ('__all__')

class AnonymousUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousPersonalData
        fields = ('__all__')

class OrderSerializer(serializers.ModelSerializer):
    
    personal_user_data = UserDataSerializer()
    anonymous_user_data = AnonymousUserDataSerializer()
    
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
            'personal_user_data',
            'visto',
            'mercado_pago_approved',
            'pago',
            'anonymous_user_data',
            'envio',
        )

class OrdenDetailSerilizer(serializers.ModelSerializer):

    order = OrderSerializer()

    class Meta:
        model = Order_detail
        fields=(
            'order',
            'product',
            'quantity',
            )

