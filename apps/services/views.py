from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination
from django.db.models import Count
from django.http.response import JsonResponse
import datetime
import json
import mercadopago
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from .serializers import (
    ServicesSerializer,
    ServicesDetailSerializer,
    BookingSerializer,
    BookingSerializerToList,
    ServiceAndApoimentsSerializer,
    ServiceBreakSerializer,
    AnonymousPersonalServiceDataSerializer,
    UpdateBookingVisteSerializer,
    ClearBookingsNoVistasSerializer,
    BookingSerializerForUser,
    CreateBookingSerializer,
    OnlyTiendaIdSerializer,
    CategoriesSerializer,
    CategoriesSerializerPrivate,
    ServicesSerializerPrivate,
    CreateServicesSerializer,
    ImageSerializer,
    UpdatePublicStatusService,
    UpdateService,
    PortadaServiceImageSerializer,
    ServicesPublicSerializer,
    OpinionCreateSerializer,
    OpinionListSerializer,
    UserOpinionUpdateSerializer,
    PreguntaServiceSerializer,
    PreguntaCreateSerializer,
    PreguntaServiceAdminSerializer,
    PreguntaUpdateSerializer,
    ClearServiceQuestionsNoVistasSerializer,
    ListCategoriesSerializer,
    MercadoPagoSerializer,
    BookingMercadoPagoDetailSerializer,
    UpdateBookingCompletedSerializer
)

# Permisos
from rest_framework import permissions

from .permissions import (
    CanCreateService,
    CanCreateCategorie,
    IsHe,
    IsHe_2,
    isOwner_category,
    isOwner_service,
    isOwner_image,
    CanCreateMoreImages,
)
from .models import (
    Booking,
    Service,
    Category_Service,
    Service_Images,
    OpinionesServices,
    PreguntaService,
    BookingMercadoPagoDetail
)
from apps.tiendas.models import Tienda, Plan, MercadoPago

# Create your views here.


class Pagination100(pagination.PageNumberPagination):
    page_size = 100


class ServicesList(ListAPIView):
    serializer_class = ServicesSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Service.objects.filter(
            tienda=tienda,
            public=True,
            portada=True,
        )


class ServiceDetailView(RetrieveAPIView):
    serializer_class = ServicesDetailSerializer

    def get_queryset(self):
        return Service.objects.all()


class CreateBooking(CreateAPIView):
    serializer_class = CreateBookingSerializer

    def post(self, request, *args, **kwargs):

        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tienda_request = serializer.validated_data["tienda"]

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list("plan", flat=True)

        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db = Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_bookings_allow = plan_db.bookings
            print(cant_bookings_allow)

            existe_bookings = Booking.objects.filter(service__tienda=tienda_request)

            if existe_bookings.exists():

                today = datetime.datetime.now()
                mes = today.strftime("%m")

                cuento = Booking.objects.filter(
                    service__tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_bookings_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_bookings_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)

                if cantidad_bookings_por_mes >= cant_bookings_allow:
                    return Response(
                        {"msj": "limite excedido"}, status=HTTP_401_UNAUTHORIZED
                    )
                else:

                    Booking.objects.create(
                        service=serializer.validated_data["service"],
                        user_personal_data=serializer.validated_data[
                            "user_personal_data"
                        ],
                        anonymous_personal_service_data=serializer.validated_data[
                            "anonymous_personal_service_data"
                        ],
                        date=serializer.validated_data["date"],
                        time=serializer.validated_data["time"],
                        completed=True,
                    )
                    
                    return Response({"msj": "puede crear"}, status=HTTP_200_OK)
            else:
                Booking.objects.create(
                    service=serializer.validated_data["service"],
                    user_personal_data=serializer.validated_data["user_personal_data"],
                    anonymous_personal_service_data=serializer.validated_data[
                        "anonymous_personal_service_data"
                    ],
                    date=serializer.validated_data["date"],
                    time=serializer.validated_data["time"],
                    completed=True,
                )
                return Response({"msj": "no existe booking"}, status=HTTP_200_OK)


class CreateBookingWithPayment(CreateAPIView):
    serializer_class = CreateBookingSerializer

    def post(self, request, *args, **kwargs):

        resp = {"booking_id": 0}

        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tienda_request = serializer.validated_data["tienda"]

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list("plan", flat=True)

        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db = Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_bookings_allow = plan_db.bookings
            print(cant_bookings_allow)

            existe_bookings = Booking.objects.filter(service__tienda=tienda_request)

            if existe_bookings.exists():

                today = datetime.datetime.now()
                mes = today.strftime("%m")

                cuento = Booking.objects.filter(
                    service__tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_bookings_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_bookings_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)

                if cantidad_bookings_por_mes >= cant_bookings_allow:
                    return Response(
                        {"msj": "limite excedido"}, status=HTTP_401_UNAUTHORIZED
                    )
                else:

                    booking_create = Booking.objects.create(
                        service=serializer.validated_data["service"],
                        user_personal_data=serializer.validated_data[
                            "user_personal_data"
                        ],
                        anonymous_personal_service_data=serializer.validated_data[
                            "anonymous_personal_service_data"
                        ],
                        date=serializer.validated_data["date"],
                        time=serializer.validated_data["time"],
                        completed=False,
                    )

                    res = {"booking_id": booking_create.id}

                    return Response(res, status=HTTP_200_OK)
            else:
                booking_create = Booking.objects.create(
                    service=serializer.validated_data["service"],
                    user_personal_data=serializer.validated_data["user_personal_data"],
                    anonymous_personal_service_data=serializer.validated_data[
                        "anonymous_personal_service_data"
                    ],
                    date=serializer.validated_data["date"],
                    time=serializer.validated_data["time"],
                    completed=False,
                )
                res = {"booking_id": booking_create.id}

                return Response(res, status=HTTP_200_OK)

class MercadoPagoInitPoint(APIView):
    def post(self, request):
        serializer = MercadoPagoSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_id = serializer.validated_data["tienda_id"]
        tienda = serializer.validated_data["tienda"]
        total = float(serializer.validated_data["total"])
        booking = serializer.validated_data["booking"]

        title = "Compra en " + serializer.validated_data["tienda"]

        # En produccion 'https://mitienda.app/'
        # en desaroolo 'http://127.0.0.1:8080/'
        prod="https://mitienda.app/"
        local = "http://127.0.0.1:8080/"

        current_site = prod

        mercadopago_db = MercadoPago.objects.get(tienda=tienda_id)

        access_token = mercadopago_db.access_token

        url_success = (
            str(current_site) + str(tienda) + "/user/booking/detail/" + str(booking)
        )
        url_failure = (
            str(current_site) + str(tienda) + "/user/booking/detail/" + str(booking)
        )
        url_pending = (
            str(current_site) + str(tienda) + "/user/booking/detail/" + str(booking)
        )

        sdk = mercadopago.SDK(access_token)

        preference_data = {
            "external_reference": booking,
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
        booking = serializer.validated_data["booking"]

        title = "Compra en " + serializer.validated_data["tienda"]

        # En produccion 'https://mitienda.app/'
        # en desaroolo 'http://127.0.0.1:8080/'
        prod="https://mitienda.app/"
        local = "http://127.0.0.1:8080/"

        current_site = prod

        mercadopago_db = MercadoPago.objects.get(tienda=tienda_id)

        access_token = mercadopago_db.access_token

        url_success = (
            str(current_site) + str(tienda) + "/anon/booking/detail/" + str(booking)
        )
        url_failure = (
            str(current_site) + str(tienda) + "/anon/booking/detail/" + str(booking)
        )
        url_pending = (
            str(current_site) + str(tienda) + "/anon/booking/detail/" + str(booking)
        )

        sdk = mercadopago.SDK(access_token)

        preference_data = {
            "external_reference": booking,
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


class CreateMercadoPagoBookingDetail(CreateAPIView):
    serializer_class = BookingMercadoPagoDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = BookingMercadoPagoDetailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        create = BookingMercadoPagoDetail.objects.update_or_create(
            booking=serializer.validated_data["booking"],
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


class CanCreateBooking(APIView):
    serializer_class = OnlyTiendaIdSerializer

    def post(self, request, *args, **kwargs):

        print(request.data)
        serializer = OnlyTiendaIdSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_request = serializer.validated_data["tienda"]

        ####Ordenes

        plan_search = Tienda.objects.filter(
            id=tienda_request,
        ).values_list("plan", flat=True)

        if plan_search:
            print("plan")
            plan = plan_search[0]
            print(plan)
            plan_db = Plan.objects.get(id=plan)

            print("cantidad de ordenes permitidas")
            cant_bookings_allow = plan_db.bookings
            print(cant_bookings_allow)

            existe_bookings = Booking.objects.filter(service__tienda=tienda_request)

            if existe_bookings.exists():

                today = datetime.datetime.now()
                mes = today.strftime("%m")

                cuento = Booking.objects.filter(
                    service__tienda=tienda_request,
                    created__month=mes,
                ).count()

                cantidad_bookings_por_mes = int(cuento)

                print("cuenta")
                print(cantidad_bookings_por_mes)
                print("dateTIME today")
                print(today)
                print("MES")
                print(mes)

                if cantidad_bookings_por_mes >= cant_bookings_allow:
                    return Response(
                        {"msj": "limite excedido"}, status=HTTP_401_UNAUTHORIZED
                    )
                if cantidad_bookings_por_mes < cant_bookings_allow:
                    return Response({"msj": "limite NO excedido"}, status=HTTP_200_OK)
            else:
                return Response({"msj": "limite NO excedido"}, status=HTTP_200_OK)


class FilterDate(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date", "")
        service = self.request.query_params.get("service", "")

        return Booking.objects.filter(date=date, service=service,completed=True)


class GetCategoriesParents(ListAPIView):
    serializer_class = ListCategoriesSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")

        return Category_Service.objects.filter(tienda=tienda, parent=None)


class GetSubCategories(ListAPIView):
    serializer_class = ListCategoriesSerializer

    def get_queryset(self):
        id = self.request.query_params.get("id", "")
        return Category_Service.objects.filter(parent__id=id)


class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return Category_Service.objects.all()


class GetServicesOfCategory(ListAPIView):
    serializer_class = ServicesSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category", "")
        return Service.objects.filter(category=category)


class ServiceDetailViewAdmin(RetrieveAPIView):
    serializer_class = ServicesSerializerPrivate

    def get_queryset(self):
        return Service.objects.all()


class CantImagesOffService(APIView):
    def get(self, request):
        service = self.request.query_params.get("service", "")
        cant_images = (
            Service_Images.objects.filter(service=service)
            .values("service")
            .annotate(cantidad=Count("id"))
        )

        dict_res = {
            "cant_images": 0,
        }

        dict_res["cant_images"] = cant_images[0]["cantidad"]

        return Response(dict_res, status=status.HTTP_200_OK)


###ADMIN


class GetAllServicesAndApoimentsToCalendar(ListAPIView):
    serializer_class = ServiceAndApoimentsSerializer
    pagination_class = Pagination100

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")

        return Service.objects.filter(tienda=tienda).order_by("-created")


class GetApoimentsFromADate(ListAPIView):
    serializer_class = BookingSerializer
    pagination_class = Pagination100

    def get_queryset(self):
        service = self.request.query_params.get("service", "")
        date = self.request.query_params.get("date", "")

        return Booking.objects.filter(service=service, date__gt=date)


class ListServicesAdmin(ListAPIView):
    serializer_class = ServicesSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Service.objects.filter(tienda=tienda)


class CreateService(CreateAPIView):
    serializer_class = CreateServicesSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateService]


class UpdateService(UpdateAPIView):
    serializer_class = UpdateService
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_service]
    queryset = Service.objects.all()


class GetImagesOffService(ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        service = self.kwargs.get("service", None)
        return Service_Images.objects.filter(service=service)


class UpadatePublicStatusService(UpdateAPIView):
    serializer_class = UpdatePublicStatusService
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_service]
    queryset = Service.objects.all()


class DeleteService(DestroyAPIView):
    serializer_class = ServicesSerializer
    queryset = Service.objects.all()


class ServiceBreakUpdate(UpdateAPIView):
    serializer_class = ServiceBreakSerializer
    queryset = Service.objects.all()


class GetNewsBookingOffTienda(ListAPIView):
    serializer_class = BookingSerializerToList

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Booking.objects.filter(service__tienda=tienda, visto=False, completed=True).order_by(
            "-created"
        )


class CreateAnonymousPersonalServiceData(CreateAPIView):
    serializer_class = AnonymousPersonalServiceDataSerializer


class CountNewsOrders(APIView):
    def get(self, request):
        tienda = self.request.query_params.get("tienda", "")
        dict_res = {
            "reservas_nuevas": 0,
        }

        existe_ordenes = Booking.objects.filter(service__tienda=tienda, visto=False, completed=True)

        if existe_ordenes.exists():

            ordenes_news = (
                Booking.objects.filter(service__tienda=tienda, visto=False, completed=True)
                .values("visto")
                .annotate(ordenes=Count("visto"))
            )
            dict_res["reservas_nuevas"] = ordenes_news[0]["ordenes"]

        return Response(dict_res, status=status.HTTP_200_OK)


class UpdateBookingVisto(UpdateAPIView):
    serializer_class = UpdateBookingVisteSerializer
    queryset = Booking.objects.all()

class UpdateBookingCompleted(UpdateAPIView):
    serializer_class = UpdateBookingCompletedSerializer
    queryset = Booking.objects.all()

#este es para admin,faltan permisos
class ViewBooking(RetrieveAPIView):
    serializer_class = BookingSerializerToList
    queryset = Booking.objects.all()

#este es para USER,faltan permisos
class UserViewBooking(RetrieveAPIView):
    serializer_class = BookingSerializerToList
    queryset = Booking.objects.all()


class DeleteBooking(DestroyAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


class ClearOrdersNoVistas(APIView):

    serializer_class = ClearBookingsNoVistasSerializer

    def post(self, request, *args, **kwargs):

        serializer = ClearBookingsNoVistasSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda_id"]

        bookings_db = Booking.objects.filter(
            service__tienda=tienda, visto=False
        ).update(visto=True)

        print(bookings_db)

        return Response({"msj": "OK"}, status=HTTP_200_OK)


""" User """

""" faltan permisos! """


class BookingsByUser(ListAPIView):
    serializer_class = BookingSerializerForUser

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        return Booking.objects.filter(user_personal_data__user=user).order_by(
            "-created"
        )


class BookingsByUserByTienda(ListAPIView):
    serializer_class = BookingSerializerForUser

    def get_queryset(self):
        user = self.request.query_params.get("user", None)
        tienda = self.request.query_params.get("tienda", None)
        return Booking.objects.filter(
            service__tienda=tienda, user_personal_data__user=user
        ).order_by("-created")


""" CATEGORIAS """


class GetCategoriesParentsPrivate(ListAPIView):
    serializer_class = CategoriesSerializerPrivate
    permission_classes = [permissions.IsAuthenticated, IsHe]

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")

        return Category_Service.objects.filter(tienda=tienda, parent=None)


class GetSubCategoriesPrivate(ListAPIView):
    serializer_class = CategoriesSerializerPrivate
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        id = self.request.query_params.get("id", "")
        return Category_Service.objects.filter(parent__id=id)


class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return Category_Service.objects.all()


class GetServicesOfCategoryPrivate(ListAPIView):
    serializer_class = ServicesSerializerPrivate

    def get_queryset(self):
        category = self.request.query_params.get("category", "")
        return Service.objects.filter(category=category)


class CreateCategorie(CreateAPIView):
    serializer_class = CategoriesSerializerPrivate
    permission_classes = [permissions.IsAuthenticated, CanCreateCategorie]


class DeleteCategoria(DestroyAPIView):
    serializer_class = CategoriesSerializerPrivate
    permission_classes = [permissions.IsAuthenticated, isOwner_category]
    queryset = Category_Service.objects.all()


class UpdateCategoria(UpdateAPIView):
    serializer_class = CategoriesSerializerPrivate
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_category]
    queryset = Category_Service.objects.all()


""" CATEGORIAS """


""" Mas Imagenes """

# Multiple image uploads
def modify_input_for_multiple_files(service, image, tienda):
    dict = {}
    dict["service"] = service
    dict["image"] = image
    dict["tienda"] = tienda
    return dict


class CreateMoreServiceImages(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated,
        CanCreateMoreImages,
        isOwner_service,
    ]

    def get(self, request):
        all_images = Service_Images.objects.all()
        serializer = ImageSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        service = request.data["service"]
        tienda = request.data["tienda"]

        # converts querydict to original dict
        images = dict((request.data).lists())["image"]
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(service, img_name, tienda)
            file_serializer = ImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class DeleteServiceImages(DestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_image]
    queryset = Service_Images.objects.all()


class UpdatePortadaServiceImage(UpdateAPIView):
    serializer_class = PortadaServiceImageSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_service]
    queryset = Service.objects.all()


class UpdateServicesImages(UpdateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_image]
    queryset = Service_Images.objects.all()


class SearchServicePrivateOnCategoryTriagram(ListAPIView):
    serializer_class = ServicesSerializerPrivate

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        category = self.request.query_params.get("category", "")
        return Service.objects.filter(
            title__trigram_similar=kword,
            category=category,
            public=True,
        )


""" NO PRIVATE, PUBLIC """


class SearchServiceTiendaTriagram(ListAPIView):
    serializer_class = ServicesPublicSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")
        return Service.objects.filter(
            title__trigram_similar=kword,
            tienda=tienda,
            public=True,
        )


class SearchOnTiendaServiceCategoryTriagram(ListAPIView):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")

        return Category_Service.objects.filter(
            name__trigram_similar=kword, tienda=tienda
        )


class HasSubCategories(ListAPIView):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category", "")
        tienda = self.request.query_params.get("tienda", "")

        return Category_Service.objects.filter(parent=category, tienda=tienda)


class SearchServiceOnCategoryTriagram(ListAPIView):
    serializer_class = ServicesSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        category = self.request.query_params.get("category", "")
        return Service.objects.filter(
            title__trigram_similar=kword,
            category=category,
            public=True,
        )


""" opiniones """


class CreateOpinion(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        serializer = OpinionCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        service_request = serializer.validated_data["service"]

        print(user)

        existe_opinion = OpinionesServices.objects.filter(
            user=user, service=service_request
        )

        if existe_opinion.exists():

            return Response({"msj": "Ya ha comentado"}, status=HTTP_200_OK)

        else:
            OpinionesServices.objects.create(
                service=service_request,
                user=user,
                rating=serializer.validated_data["rating"],
                opinion=serializer.validated_data["opinion"],
            )

            return Response({"msj": "Comentario Creado!"}, status=HTTP_200_OK)


class GetOpinionesDeService(ListAPIView):
    serializer_class = OpinionListSerializer

    def get_queryset(self):
        service = self.request.query_params.get("service")

        return OpinionesServices.objects.filter(service=service).order_by("created")


class GetUserOpinion(ListAPIView):
    serializer_class = OpinionListSerializer

    def get_queryset(self):
        service = self.request.query_params.get("service")
        user = self.request.query_params.get("user")
        return OpinionesServices.objects.filter(service=service, user=user)[0:1]


class DeleteUserOpinion(DestroyAPIView):
    serializer_class = OpinionListSerializer
    queryset = OpinionesServices.objects.all()


class UpdateUserOpinion(UpdateAPIView):
    serializer_class = UserOpinionUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OpinionesServices.objects.all()


""" opiniones """

####Preguntas


class PreguntasList(ListAPIView):
    serializer_class = PreguntaServiceSerializer

    def get_queryset(self):
        service = self.request.query_params.get("service", None)
        return PreguntaService.objects.filter(service=service).order_by("-created")


class PreguntaCreate(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        serializer = PreguntaCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        service_request = serializer.validated_data["service"]

        createQuestion = PreguntaService.objects.create(
            user=user,
            service=service_request,
            pregunta=serializer.validated_data["pregunta"],
        )

        print("createQuestion")
        print(createQuestion.service.tienda.id)
        tienda_id = createQuestion.service.tienda.id

        """ Envio la noticifacion a channel """

        res = {"tienda_id": tienda_id}
        print(res)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifi", {"type": "send_notifi_question_service", "text": json.dumps(res)}
        )

        return Response({"msj": "Pregunta Creada!"}, status=HTTP_200_OK)


class GetNewsQuestionsOffTienda(ListAPIView):
    serializer_class = PreguntaServiceAdminSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return PreguntaService.objects.filter(
            service__tienda=tienda, visto=False
        ).order_by("-created")


class UpdateQuestion(UpdateAPIView):
    serializer_class = PreguntaUpdateSerializer
    queryset = PreguntaService.objects.all()


class DeleteQuestion(DestroyAPIView):
    serializer_class = PreguntaServiceAdminSerializer
    queryset = PreguntaService.objects.all()


class CountNewsCuestions(APIView):
    def get(self, request):
        tienda = self.request.query_params.get("tienda", "")
        dict_res = {
            "preguntas_nuevas_service": 0,
        }

        existe_ordenes = PreguntaService.objects.filter(
            service__tienda=tienda, visto=False
        )

        if existe_ordenes.exists():

            preguntas_news = (
                PreguntaService.objects.filter(service__tienda=tienda, visto=False)
                .values("service__tienda")
                .annotate(preguntas=Count("service__tienda"))
            )
            dict_res["preguntas_nuevas_service"] = preguntas_news[0]["preguntas"]

        return Response(dict_res, status=status.HTTP_200_OK)


class ClearServiceQuestionsNoVistas(APIView):

    serializer_class = ClearServiceQuestionsNoVistasSerializer

    def post(self, request, *args, **kwargs):

        serializer = ClearServiceQuestionsNoVistasSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]

        bookings_db = PreguntaService.objects.filter(
            service__tienda=tienda, visto=False
        ).update(visto=True)

        print(bookings_db)

        return Response({"msj": "OK"}, status=HTTP_200_OK)
