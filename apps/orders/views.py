from calendar import c
from rest_framework import status
from rest_framework import pagination

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from django.db.models import Count, Avg, Max, Min, query
from django.db.models.functions import TruncMonth
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import datetime


from .serializers import (
    OrderSerializer,
    ProcesoOrderSerializer,
    OrderVistoSerializer,
    MercadoPagoSerializer,
    OrderUpdataMetodoPagoStatus,
    MercadoPagoDetailSerializer,
    CancelarOrdenSerializer,
    OrderEstadoSereializer,
    OrderPagoEstadoSereializer,
    AnonymousUserDataSerializer,
    ProcesoOrderAnonymousSerializer,
    ClearOrdersNoVistasSerializer,
    OnlyTiendaIdSerializer,


)
from .models import AnonymousPersonalData, Order, Order_detail, OrderMercadoPagoDetail
from rest_framework.response import Response
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework import permissions
from apps.products.models import Product, Variaciones
from apps.tiendas.models import Envios, Tienda, MercadoPago
from apps.users.models import UserPersonalData
from apps.tiendas.models import Plan


from apps.orders import serializers

""" from rest_framework.renderers import JSONRenderer """
from .permissions import IsHe, isHeRetrive

import mercadopago


# Create your views here.
class Pagination100(pagination.PageNumberPagination):
    page_size = 100


class ClearOrdersNoVistas(APIView):

    serializer_class = ClearOrdersNoVistasSerializer
    
    def post(self, request, *args, **kwargs):

        serializer = ClearOrdersNoVistasSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda =serializer.validated_data["tienda_id"]

        ordenes_db = Order.objects.filter(
            tienda=tienda,
            visto=False
        ).update(visto=True)

        print(ordenes_db)

        return Response({"msj":"OK"}, status=HTTP_200_OK)


class CanCreateOrderByPlan(APIView):
    serializer_class = OnlyTiendaIdSerializer

    def post(self, request, *args, **kwargs):


        print(request.data)
        serializer = OnlyTiendaIdSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_request = serializer.validated_data["tienda"]


        ####Ordenes

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list('plan',flat=True)
        
        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db= Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_orders_allow = plan_db.orders
            print(cant_orders_allow)


        
            existe_orders = Order.objects.filter(tienda=tienda_request)

            if existe_orders.exists():

                today = datetime.datetime.now()
                mes = today.strftime('%m')
                


                cuento = Order.objects.filter(
                    tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_ordenes_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_ordenes_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)
            
                
                if (cantidad_ordenes_por_mes >= cant_orders_allow):
                    return Response({'msj':"limite excedido"},status=HTTP_401_UNAUTHORIZED)
                if (cantidad_ordenes_por_mes < cant_orders_allow):
                    return Response({'msj':"limite NO excedido"},status=HTTP_200_OK)
            else:
                return Response({'msj':"limite NO excedido"},status=HTTP_200_OK)


class RegistrarOrden(CreateAPIView):
    serializer_class = ProcesoOrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print("entro aca?")

        print(request.data)
        serializer = ProcesoOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_db = Tienda.objects.get(id=serializer.validated_data["tienda"])

        user_personal_data_db = UserPersonalData.objects.get(user=self.request.user)

        tienda_request = serializer.validated_data["tienda"]

        ###envio instance
        envio_request = serializer.validated_data["envio"]
        print("ENVIO REQUEST")
        print(envio_request)

        if (envio_request == None):
            envio_intance = None
        else:
            envio_request = int(envio_request)
            envio_intance = Envios.objects.get(id=envio_request)
        print("envio_request")
        print(envio_request)
        print("envio_intance")

        print(envio_intance)


        ####Ordenes

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list('plan',flat=True)
        
        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db= Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_orders_allow = plan_db.orders
            print(cant_orders_allow)


        
            existe_orders = Order.objects.filter(tienda=tienda_request)

            if existe_orders.exists():

                today = datetime.datetime.now()
                mes = today.strftime('%m')

                dic = {
                    "cantidad":0
                } 

                cuento = Order.objects.filter(
                    tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_ordenes_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_ordenes_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)
            
                
                if (cantidad_ordenes_por_mes >= cant_orders_allow):
                    return Response({'msj':"limite excedido"},status=HTTP_401_UNAUTHORIZED)

        ####Ordenes


        orden = Order.objects.create(
            tienda=tienda_db,
            user=self.request.user,
            total=serializer.validated_data["total"],
            metodo_pago=serializer.validated_data["metodo_pago"],
            quantity_products=serializer.validated_data["quantity_products"],
            personal_user_data=user_personal_data_db,
            envio= envio_intance,
        )

        productos = serializer.validated_data["productos"]

        ventas_detalle = []
        variacion_to_save_db = None
        opciones_to_save_db =None
        print("productos")
        print(productos)
        precio = 0
        for prod in productos:
            count = prod["quantity"]
            resta = int(count)
            producto_db = Product.objects.get(id=prod["id"])
            print("prod")
            print(prod)
            if "variacion_id" in prod:
                variacion = Variaciones.objects.get(id=prod["variacion_id"])
                if variacion.no_stock == False:
                    variacion.stock = variacion.stock - resta
                precio = variacion.price
                print(variacion)
                variacion.save()
                variacion_to_save_db = prod["variacion_id"]
            else:
                print("product_db")
                print(producto_db)
                if producto_db.in_offer == True:
                    precio = producto_db.in_offer_price
                    if producto_db.no_stock == False:
                        producto_db.stock = producto_db.stock - resta
                    producto_db.save()
                else:
                    precio = producto_db.price
                    if producto_db.no_stock == False:
                        producto_db.stock = producto_db.stock - resta
                    producto_db.save()

            if "opciones" in prod:
                opciones_to_save_db = prod["opciones"]
            else:
                opciones_to_save_db = None

            order_detail = Order_detail(
                order=orden,
                product=producto_db,
                quantity=prod["quantity"],
                price_sale=precio,
                price_off=producto_db.in_offer_price,
                variacion_id=variacion_to_save_db,
                options=opciones_to_save_db
            )
            ventas_detalle.append(order_detail)

        orden.save()

        Order_detail.objects.bulk_create(ventas_detalle)

        """ Envio la noticifacion a channel """

        res = {"tienda_id": tienda_db.id}
        print(res)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifi", {"type": "send_notifi", "text": json.dumps(res)}
        )

        dict_res = {"orden_id": orden.id, "mensaje": "OK"}

        return Response(dict_res, status=HTTP_200_OK)


class RegistrarOrdenAnonymous(CreateAPIView):
    serializer_class = ProcesoOrderAnonymousSerializer

    def create(self, request, *args, **kwargs):

        print(request.data)
        serializer = ProcesoOrderAnonymousSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_db = Tienda.objects.get(id=serializer.validated_data["tienda"])

        anonymous_user_data_db = AnonymousPersonalData.objects.get(
            id=serializer.validated_data["anonymous_user_data"]
        )

        tienda_request = serializer.validated_data["tienda"]

        ###envio instance
        envio_request = serializer.validated_data["envio"]
        print("ENVIO REQUEST")
        print(envio_request)

        if (envio_request == None):
            envio_intance = None
        else:
            envio_request = int(envio_request)
            envio_intance = Envios.objects.get(id=envio_request)
        print("envio_request")
        print(envio_request)
        print("envio_intance")

        print(envio_intance)



        ####Ordenes

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list('plan',flat=True)
        
        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db= Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_orders_allow = plan_db.orders
            print(cant_orders_allow)


        
            existe_orders = Order.objects.filter(tienda=tienda_request)

            if existe_orders.exists():

                today = datetime.datetime.now()
                mes = today.strftime('%m')

                dic = {
                    "cantidad":0
                } 

                cuento = Order.objects.filter(
                    tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_ordenes_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_ordenes_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)
            
                
                if (cantidad_ordenes_por_mes >= cant_orders_allow):
                    return Response({'msj':"limite excedido"},status=HTTP_401_UNAUTHORIZED)

        ####Ordenes

        orden = Order.objects.create(
            tienda=tienda_db,
            total=serializer.validated_data["total"],
            metodo_pago=serializer.validated_data["metodo_pago"],
            quantity_products=serializer.validated_data["quantity_products"],
            anonymous_user_data=anonymous_user_data_db,
            envio = envio_intance
            
        )

        productos = serializer.validated_data["productos"]

        ventas_detalle = []
        variacion_to_save_db = None
        opciones_to_save_db =None
        print("productos")
        print(productos)
        precio = 0
        for prod in productos:
            count = prod["quantity"]
            resta = int(count)
            producto_db = Product.objects.get(id=prod["id"])
            print("prod")
            print(prod)
            if "variacion_id" in prod:
                variacion = Variaciones.objects.get(id=prod["variacion_id"])
                if variacion.no_stock == False:
                    variacion.stock = variacion.stock - resta
                precio = variacion.price
                print(variacion)
                variacion.save()
                variacion_to_save_db = prod["variacion_id"]
            else:
                print("product_db")
                print(producto_db)
                if producto_db.in_offer == True:
                    precio = producto_db.in_offer_price
                    producto_db.stock = producto_db.stock - resta
                    producto_db.save()
                else:
                    precio = producto_db.price
                    producto_db.stock = producto_db.stock - resta
                    producto_db.save()

            if "opciones" in prod:
                opciones_to_save_db = prod["opciones"]
            else:
                opciones_to_save_db = None

            order_detail = Order_detail(
                order=orden,
                product=producto_db,
                quantity=prod["quantity"],
                price_sale=precio,
                price_off=producto_db.in_offer_price,
                variacion_id=variacion_to_save_db,
                options=opciones_to_save_db
            )
            ventas_detalle.append(order_detail)

        orden.save()
        Order_detail.objects.bulk_create(ventas_detalle)

        """ Envio la noticifacion a channel """
        res = {"tienda_id": tienda_db.id}
        print(res)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifi", {"type": "send_notifi", "text": json.dumps(res)}
        )

        dict_res = {"orden_id": orden.id, "mensaje": "OK"}

        return Response(dict_res, status=HTTP_200_OK)


class CancelarOrden(APIView):
    serializer_class = CancelarOrdenSerializer

    def post(self, request, *args, **kwargs):

        serializer = CancelarOrdenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order_db = Order.objects.get(id=serializer.validated_data["order_id"])
        order_db.estado = "cancelada"

        productos = serializer.validated_data["productos"]

        print("order_db")
        print(order_db)
        print("productos")
        print(productos)

        # RESTAURO STOCK

        for prod in productos:
            count = prod["quantity"]
            suma = int(count)
            producto_db = Product.objects.get(id=prod["id"])
            print("prod")
            print(prod)
            if prod["variacion_id"] != None:
                variacion = Variaciones.objects.get(id=prod["variacion_id"])
                if variacion.no_stock == False:
                    variacion.stock = variacion.stock + suma
                variacion.save()
            else:
                print("product_db")
                print(producto_db)
                if producto_db.in_offer == True:
                    if producto_db.no_stock == False:
                        producto_db.stock = producto_db.stock + suma
                    producto_db.save()
                else:
                    if producto_db.no_stock == False:
                        producto_db.stock = producto_db.stock + suma
                    producto_db.save()

        order_db.save()

        dict_res = {"orden_id": order_db.id, "mensaje": "cancelled"}

        return Response(dict_res, status=HTTP_200_OK)


class OrderEstadoChange(UpdateAPIView):
    serializer_class = OrderEstadoSereializer
    queryset = Order.objects.all()


class OrderPagoChange(UpdateAPIView):
    serializer_class = OrderPagoEstadoSereializer
    queryset = Order.objects.all()


# Order list for user


class OrderListForUser(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsHe)

    def get_queryset(self):
        user = self.request.query_params.get("user", None)

        return Order.objects.filter(
            user=user
        ).order_by("-created")

class OrderListForUserByTienda(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsHe)

    def get_queryset(self):
        user = self.request.query_params.get("user", None)
        tienda = self.request.query_params.get("tienda", None)

        user = int(user)
        tienda = int(tienda)

        return Order.objects.filter(
            user=user,
            tienda=tienda
        ).order_by("-created")
# Order Detail


class OrderDetail(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.all()


class OrderDetailAnonymous(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()


####ADMIN##############


class GetOrdersOffTienda(ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = Pagination100

    def get_queryset(self):
        tienda = self.kwargs.get("tienda", None)
        return Order.objects.filter(tienda=tienda).order_by("-created")


class GetOrdersNewsOffTienda(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Order.objects.filter(tienda=tienda, visto=False).order_by("-created")


class CountNewsOrders(APIView):
    def get(self, request):
        tienda = self.request.query_params.get("tienda", "")
        dict_res = {
            "ordenes_nuevas": 0,
        }

        existe_ordenes = Order.objects.filter(tienda=tienda, visto=False)

        if existe_ordenes.exists():

            ordenes_news = (
                Order.objects.filter(tienda=tienda, visto=False)
                .values("tienda")
                .annotate(ordenes=Count("tienda"))
            )
            dict_res["ordenes_nuevas"] = ordenes_news[0]["ordenes"]

        return Response(dict_res, status=status.HTTP_200_OK)


class UpdateOrdenVisto(APIView):
    serializer_class = OrderVistoSerializer

    def put(self, request):
        serializer = OrderVistoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order_request = request.data["order_id"]

        order_db = Order.objects.get(id=order_request)
        order_db.visto = True
        order_db.estado = "Visto"
        order_db.save()

        print(order_db)

        return Response({"msj": "update"}, status=status.HTTP_200_OK)


######MERCADOPAGO


class MercadoPagoInitPoint(APIView):
    def post(self, request):
        serializer = MercadoPagoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_id = serializer.validated_data["tienda_id"]
        tienda = serializer.validated_data["tienda"]
        total = float(serializer.validated_data["total"])
        orden = serializer.validated_data["orden"]

        title = "Compra en " + serializer.validated_data["tienda"]

        # En produccion 'https://mitienda.app/'
        # en desaroolo 'http://127.0.0.1:8080/'

        current_site = "https://mitienda.app/"

        mercadopago_db = MercadoPago.objects.get(tienda=tienda_id)

        access_token = mercadopago_db.access_token

        url_success = (
            str(current_site) + str(tienda) + "/user/order/detail/" + str(orden)
        )
        url_failure = (
            str(current_site) + str(tienda) + "/user/order/detail/" + str(orden)
        )
        url_pending = (
            str(current_site) + str(tienda) + "/user/order/detail/" + str(orden)
        )

        sdk = mercadopago.SDK(access_token)

        preference_data = {
            "external_reference": orden,
            "items": [
                {
                    "title": title,
                    "quantity": 1,
                    "unit_price": total,
                }
            ],
            "back_urls": {
                "success": url_success,
                "failure": url_failure,
                "pending": url_pending,
            },
            "auto_return": "all",
            "payment_methods": {
                "excluded_payment_methods": [{"id": "pagofacil"}, {"id": "rapipago"}],
                "excluded_payment_types": [{"id": "ticket"}],
                "installments": 12,
            },
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        print(preference)

        return Response(preference, status=HTTP_200_OK)


class MercadoPagoInitPointAnonymous(APIView):
    def post(self, request):
        serializer = MercadoPagoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_id = serializer.validated_data["tienda_id"]
        tienda = serializer.validated_data["tienda"]
        total = float(serializer.validated_data["total"])
        orden = serializer.validated_data["orden"]

        title = "Compra en " + serializer.validated_data["tienda"]

        # En produccion 'https://mitienda.app/'
        # en desaroolo 'http://127.0.0.1:8080/'

        current_site = "https://mitienda.app/"

        mercadopago_db = MercadoPago.objects.get(tienda=tienda_id)

        access_token = mercadopago_db.access_token

        url_success = (
            str(current_site) + str(tienda) + "/anon/order/detail/" + str(orden)
        )
        url_failure = (
            str(current_site) + str(tienda) + "/anon/order/detail/" + str(orden)
        )
        url_pending = (
            str(current_site) + str(tienda) + "/anon/order/detail/" + str(orden)
        )

        sdk = mercadopago.SDK(access_token)

        preference_data = {
            "external_reference": orden,
            "items": [
                {
                    "title": title,
                    "quantity": 1,
                    "unit_price": total,
                }
            ],
            "back_urls": {
                "success": url_success,
                "failure": url_failure,
                "pending": url_pending,
            },
            "auto_return": "all",
            "payment_methods": {
                "excluded_payment_methods": [{"id": "pagofacil"}, {"id": "rapipago"}],
                "excluded_payment_types": [{"id": "ticket"}],
                "installments": 12,
            },
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        print(preference)

        return Response(preference, status=HTTP_200_OK)


class UpdateOrderMercadoPagoStatus(UpdateAPIView):
    serializer_class = OrderUpdataMetodoPagoStatus
    queryset = Order.objects.all()


class CreateMercadoPagoOrderDetail(CreateAPIView):
    serializer_class = MercadoPagoDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = MercadoPagoDetailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        create = OrderMercadoPagoDetail.objects.update_or_create(
            order=serializer.validated_data["order"],
            collection_id=serializer.validated_data["collection_id"],
            collection_status=serializer.validated_data["collection_status"],
            payment_id=serializer.validated_data["payment_id"],
            payment_type=serializer.validated_data["payment_type"],
            merchant_order_id=serializer.validated_data["merchant_order_id"],
            external_reference=serializer.validated_data["external_reference"],
        )
        print("que hay en create")
        print(create[1])

        if create[1] == True:
            return Response({"mensaje": "Detail Creado"}, status=status.HTTP_200_OK)
        if create[1] == False:
            return Response(
                {"mensaje": "Detail Actualizado"}, status=status.HTTP_200_OK
            )


class MercadoPagoDetail(ListAPIView):
    serializer_class = MercadoPagoDetailSerializer

    def get_queryset(self):
        order = self.request.query_params.get("order", "")
        return OrderMercadoPagoDetail.objects.filter(order=order)


class SearchOrderByDate(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        date = self.request.query_params.get("date", "")
        return Order.objects.filter(tienda=tienda, created__icontains=date)


class SearchOrderById(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        id = self.request.query_params.get("id", "")
        return Order.objects.filter(tienda=tienda, id=id)


class FilterOrdersVistas(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Order.objects.filter(tienda=tienda, visto=False)


class DeleteOrder(DestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class CreateAnonymousData(CreateAPIView):
    serializer_class = AnonymousUserDataSerializer

