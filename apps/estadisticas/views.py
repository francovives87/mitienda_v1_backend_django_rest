from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED,HTTP_400_BAD_REQUEST
from django.db.models import Count, Avg, Max, Min, query,Sum

#MODELS
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
#SERIALIZERS
from .serializers import (
 GenericStaticsSerializer,
 OrdenDetailSerilizer,
 OrderSerializer
)

# Create your views here.

class ListCantProductsOnOrder(ListAPIView):
    serializer_class = GenericStaticsSerializer
    def post(self, request):
        rest_dict={
            "total_ordenes" : None,
            "total_ordenes_payment_completed":None
        }

        pendiente="pendiente"
        pago_completado="completado"

        serializer = GenericStaticsSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]


        cant_total_quantity_orders = Order_detail.objects.filter(
            product = product,
        ).aggregate(Sum('quantity'))

        cant_total_quantity_orders_pay_completed = Order_detail.objects.filter(
            product = product,
            order__pago=pago_completado
        ).aggregate(Sum('quantity'))

        print("Cantidad total ordenadas")
        print(cant_total_quantity_orders)

        print("Cantidad total ordenadas y pagos completados")
        print(cant_total_quantity_orders_pay_completed)

        rest_dict = {
            "total_ordenes" : cant_total_quantity_orders["quantity__sum"],
            "total_ordenes_payment_completed" : cant_total_quantity_orders_pay_completed["quantity__sum"]
        }
        

        return Response(rest_dict, status=status.HTTP_201_CREATED)

class ListOrdersWhereHaveProduct(ListAPIView):
    serializer_class = OrdenDetailSerilizer
    def get_queryset(self):
        product = self.request.query_params.get("product", "")
        tienda = self.request.query_params.get("tienda", "")
        product = int(product)
        print("PRODUCT")
        print(product)
        print("TIENDA")
        print(tienda)
        #UNA SEGURIDAD QUE LO PONGO YO, SI NO ENVIA LA TIENDA ID PARA VERIFICAR EL PERMISO,
        #NO ARRJO NINGUN RESULTADO!
        if tienda == "":
            return Order_detail.objects.filter(
            product = None
        ).order_by("-created")
        return Order_detail.objects.filter(
            product = product
        ).order_by("-created")



""" class ListOrdersWhereHaveProduct(APIView):
    #CREAR EL ListAPIView a partir del APIView!!!!!
    #un año me costo,
    #esta es la manera de pedir datos con un serializador, este devuvlce un queryset.model
    #que luego lo paso por un serializador model y me lo formatea y devulve como quiero!!
    
    def post(self, request, format=None):
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        serializer = GenericStaticsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]

        query = Order_detail.objects.filter(
            product = product
        ).order_by("-created")

        print("lista de ordenes donde esta")
        print(query)
        page = paginator.paginate_queryset(query, request, view=self)

        serializer = OrdenDetailSerilizer(page,many=True)

        return Response(serializer.data) """



