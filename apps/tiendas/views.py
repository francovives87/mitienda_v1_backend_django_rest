from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)
from django.db.models import Count, Avg, Max, Min, fields
from rest_framework.views import APIView
from rest_framework import status
import json
import datetime
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.lookups import Unaccent
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import Distance
from rest_framework import pagination
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)

from apps.users.models import User
from apps.orders.models import Order
from .serializers import (
    TiendaSerializer,
    SliderSerializer,
    ColorsSerializer,
    TexturesSerializer,
    UpdateColorsTextureSerializer,
    InformacionSerializer,
    UpdateTiendaLogoSerializer,
    UpdateTiendaTituloSerializer,
    SliderPrivateSerializer,
    SliderPublicUptade,
    CreateTiendaSerializer,
    MercadoPagoCredentialExists,
    MercadoPagoCredential,
    EnvioSerializer,
    UserHasTiendaSerializer,
    TipoDeTiendaSerializer,
    FavoritosSerializer,
    FavoritesList,
    CreateQrSerializer,
    GetQrSerializer,
    GeoDjangoSerializer,
    GeoDjangoSerializerExists,
    SearchByCitySerializer,
    FilterCitiesBySubregionSerializer,
    FilterDepartamentosByRegionSerializer,
    SearchStoreByTitleGlobalSerializer,
    GeolocalizationSerializer,
    GeolocalizationUpdateSerializer,
    TiendaDestacadaSerializer,
    TiendaVisitorCreateSerializer,
    TiendaVisitorGetSerializer,
    OpinionCreateSerializer,
    OpinionListSerializer,
    UserOpinionUpdateSerializer,
    TitleFrontColorSerializer,
    TitleFontSerializer,
    TitleFontUpdate,
    PaymentMethodsUpdateSerializer,
    TransferCredentialExists,
    TransferDataCredentials,
    TiendaDemoSerializer
)
from .models import (
    Envios,
    Favoritos,
    MercadoPago,
    Slider,
    Tienda,
    Colors,
    Textures,
    Informacion,
    Codigoqr,
    Geolocalization_geodjango,
    TiendaVisitor,
    Opiniones,
    Title_font,
    PaymentMethods,
    TransferData,
)
from apps.products.models import (
    Category,
    Product,
)
from apps.blog.models import Category_blog, Entry
from apps.services.models import (
    Service,
    Booking,
)
from django.core import serializers
from django.http import HttpResponse

# Permisos
from rest_framework import permissions


from .permissions import (
    CanCreateSlide,
)


class Pagination6(pagination.PageNumberPagination):
    page_size = 6


# Create your views here.
class UserHasTienda(APIView):
    def post(self, request):
        serializer = UserHasTiendaSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            existe_tienda_para_este_user = Tienda.objects.get(
                user=serializer.validated_data["user_id"]
            )
        except Tienda.DoesNotExist:
            existe_tienda_para_este_user = None

        respuesta = {
            "tienda_id": 0,
            "name": None,
        }

        if existe_tienda_para_este_user != None:
            respuesta["tienda_id"] = existe_tienda_para_este_user.id
            respuesta["name"] = existe_tienda_para_este_user.name
            return Response(respuesta, status=status.HTTP_200_OK)
        else:
            return Response({"mensaje": "denied"}, status=status.HTTP_200_OK)


class GetTienda(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("tienda", None)
        tiendaData = Tienda.objects.filter(name=tienda)[0:1]  # solo uno

        tiendaData.avarange = 5.0

        return tiendaData


class GetTiendaByUserId(ListAPIView):
    serializer_class = TiendaSerializer

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        return Tienda.objects.filter(user=user)[0:1]


class GetSliderPublic(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("pk", None)
        return Slider.objects.GetSliderOffTienda(tienda)


class GetColorsOffTienda(ListAPIView):
    serializer_class = ColorsSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("tienda", None)
        return Colors.objects.GetColorsOffTienda(tienda)


class GetTitleFonts(ListAPIView):
    serializer_class = TitleFontSerializer
    pagination_class = Pagination6
    queryset = Title_font.objects.all().order_by("name")


class UpdateTitleFont(UpdateAPIView):
    serializer_class = TitleFontUpdate
    queryset = Colors.objects.all()


class UpdateColores(UpdateAPIView):
    serializer_class = ColorsSerializer
    queryset = Colors.objects.all()


class ListTexures(ListAPIView):
    serializer_class = TexturesSerializer

    def get_queryset(self):
        return Textures.objects.all()


class UpdateColoresWithTexture(UpdateAPIView):
    serializer_class = UpdateColorsTextureSerializer
    queryset = Colors.objects.all()


class UpdateTiendaInformation(UpdateAPIView):
    serializer_class = InformacionSerializer
    queryset = Informacion.objects.all()


class UpdateTiendaLogo(UpdateAPIView):
    serializer_class = UpdateTiendaLogoSerializer
    queryset = Tienda.objects.all()


class GetSliderPrivate(ListAPIView):
    serializer_class = SliderPrivateSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("pk", None)
        return Slider.objects.filter(tienda=tienda)


class UpdateSlider(UpdateAPIView):
    serializer_class = SliderPrivateSerializer
    queryset = Slider.objects.all()


class SliderPublicUpdate(UpdateAPIView):
    serializer_class = SliderPublicUptade
    queryset = Slider.objects.all()


class DeleteSlider(DestroyAPIView):
    serializer_class = SliderPrivateSerializer
    queryset = Slider.objects.all()


class CreateSlider(CreateAPIView):
    serializer_class = SliderPrivateSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateSlide]


class UpdateTiendaTitle(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UpdateTiendaTituloSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]
        title = serializer.validated_data["title"]

        tienda_db = Tienda.objects.filter(id=tienda).update(title=title)

        print(tienda_db)

        return Response({"mensaje": "Updated"}, status=HTTP_200_OK)


class CreateTienda(CreateAPIView):
    serializer_class = CreateTiendaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = CreateTiendaSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda_db = Tienda.objects.create(
            user=self.request.user,
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"],
            title=serializer.validated_data["title"],
        )

        colors_db = Colors.objects.create(
            tienda=tienda_db,
        )

        infromacion_db = Informacion.objects.create(
            tienda=tienda_db,
        )
        payment_methods = PaymentMethods.objects.create(tienda=tienda_db)

        tienda_db.save()
        colors_db.save()
        infromacion_db.save()
        payment_methods.save()

        return Response({"mensaje": "OK"}, status=HTTP_200_OK)


##### Admin get objects


class GetTotalObjectsCreatedOffTienda(APIView):
    def get(self, request):
        dict_res = {
            "categorias": 0,
            "productos": 0,
            "categorias_blog": 0,
            "entries_blog": 0,
            "services": 0,
            "sliders": 0,
            "orders": 0,
            "reservas": 0,
        }

        today = datetime.datetime.now()
        mes = today.strftime("%m")

        tienda = self.request.query_params.get("tienda", "")

        ###existe categoria?

        existe_categorias_product = Category.objects.filter(tienda=tienda)

        if existe_categorias_product.exists():

            categories = (
                Category.objects.filter(tienda=tienda)
                .values("tienda")
                .annotate(categorias=Count("tienda"))
            )
            dict_res["categorias"] = categories[0]["categorias"]

        ### existe product?

        existe_product = Product.objects.filter(tienda=tienda)

        if existe_product.exists():

            productos = (
                Product.objects.filter(tienda=tienda)
                .values("tienda")
                .annotate(productos=Count("tienda"))
            )
            dict_res["productos"] = productos[0]["productos"]

        ### existe categorias blog?

        existe_categorias_blog = Category_blog.objects.filter(tienda=tienda)

        if existe_categorias_blog.exists():

            categories_blog = (
                Category_blog.objects.filter(tienda=tienda)
                .values("tienda")
                .annotate(categories_blog=Count("tienda"))
            )
            dict_res["categorias_blog"] = categories_blog[0]["categories_blog"]

        ####

        existe_entrie_blog = Entry.objects.filter(tienda=tienda)

        if existe_entrie_blog:
            entries_blog = (
                Entry.objects.filter(tienda=tienda)
                .values("tienda")
                .annotate(entries_blog=Count("tienda"))
            )
            dict_res["entries_blog"] = entries_blog[0]["entries_blog"]

        ### existe servicios?

        existe_services = Service.objects.filter(tienda=tienda)

        if existe_services.exists():

            services = (
                Service.objects.filter(tienda=tienda)
                .values("tienda")
                .annotate(services=Count("tienda"))
            )
            dict_res["services"] = services[0]["services"]

        ####

        ### existe sliders?

        existe_sliders = Slider.objects.filter(tienda=tienda)

        if existe_sliders.exists():

            sliders = (
                Slider.objects.filter(tienda=tienda)
                .values("tienda")
                .annotate(sliders=Count("tienda"))
            )
            dict_res["sliders"] = sliders[0]["sliders"]

        ####

        ####Ordenes

        existe_orders = Order.objects.filter(tienda=tienda)

        if existe_orders.exists():

            orders_db = Order.objects.filter(
                tienda=tienda,
                created__month=mes,
            ).count()

            orders = int(orders_db)

            dict_res["orders"] = orders
        ####Ordenes

        ####Bookings

        existe_bookings = Booking.objects.filter(service__tienda=tienda)

        if existe_bookings.exists():

            cuento = Booking.objects.filter(
                service__tienda=tienda, created__month=mes, completed=True
            ).count()

            cantidad_bookings_por_mes = int(cuento)

            dict_res["reservas"] = cantidad_bookings_por_mes

        ####Booking

        print(dict_res)

        return Response(dict_res, status=status.HTTP_200_OK)


class TransferCredentialsExists(APIView):
    def post(self, request):

        serializer = TransferCredentialExists(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]

        existe_credencial = TransferData.objects.filter(tienda=tienda)

        if existe_credencial.exists():

            transfer_data = {
                "bank": existe_credencial[0].bank,
                "alias": existe_credencial[0].alias,
                "cbu": existe_credencial[0].cbu,
            }

            return Response(transfer_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"mensaje:": "NO existe una configuracion"},
                status=status.HTTP_404_NOT_FOUND,
            )

class TransferDataCredentialsCreateOrUpdate(APIView):
    def post(self, request):
        serializer = TransferDataCredentials(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]
        bank = serializer.validated_data["bank"]
        alias =serializer.validated_data["alias"]
        cbu= serializer.validated_data["cbu"]
        

        update_flag = False
        create_flag = False

        tienda_db = Tienda.objects.get(
            id=tienda,
        )

        existe_credencial = TransferData.objects.filter(tienda=tienda)

        if existe_credencial.exists():
            update = TransferData.objects.get(tienda=tienda)
            update.bank = bank
            update.alias = alias
            update.cbu = cbu
            update.save()
            update_flag = True
        else:
            create = TransferData.objects.create(
                tienda=tienda_db, 
                bank=bank, 
                alias=alias,
                cbu = cbu
            )
            create.save()
            create_flag = True

        if update_flag == True:
            return Response({"mensaje": "Update"}, status=status.HTTP_200_OK)
        if create_flag == True:
            return Response({"mensaje": "Created"}, status=status.HTTP_200_OK)


class MercadoPagoCredentialsExists(APIView):
    def post(self, request):

        serializer = MercadoPagoCredentialExists(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]

        existe_credencial = MercadoPago.objects.filter(tienda=tienda)

        if existe_credencial.exists():
            return Response(
                {"mensaje:": "Ya existe una configuracion"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"mensaje:": "NO existe una configuracion"},
                status=status.HTTP_404_NOT_FOUND,
            )


class MercadoPagoCredentialsCreateOrUpdate(APIView):
    def post(self, request):
        serializer = MercadoPagoCredential(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]
        public_key = serializer.validated_data["public_key"]
        access_token = serializer.validated_data["access_token"]

        update_flag = False
        create_flag = False

        tienda_db = Tienda.objects.get(
            id=tienda,
        )

        existe_credencial = MercadoPago.objects.filter(tienda=tienda)

        if existe_credencial.exists():
            update = MercadoPago.objects.get(tienda=tienda)
            update.public_key = public_key
            update.access_token = access_token
            update.save()
            update_flag = True
        else:
            create = MercadoPago.objects.create(
                tienda=tienda_db, public_key=public_key, access_token=access_token
            )
            create.save()
            create_flag = True

        if update_flag == True:
            return Response({"mensaje": "Update"}, status=status.HTTP_200_OK)
        if create_flag == True:
            return Response({"mensaje": "Created"}, status=status.HTTP_200_OK)


class CreateEnvio(CreateAPIView):
    serializer_class = EnvioSerializer


class ListEnvios(ListAPIView):
    serializer_class = EnvioSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Envios.objects.filter(tienda=tienda)


class UpdateEnvio(UpdateAPIView):
    serializer_class = EnvioSerializer
    queryset = Envios.objects.all()


class DeleteEnvio(DestroyAPIView):
    serializer_class = EnvioSerializer
    queryset = Envios.objects.all()


class TipoDeTienda(UpdateAPIView):
    serializer_class = TipoDeTiendaSerializer
    queryset = Tienda.objects.all()


class ListFavoritos(ListAPIView):
    serializer_class = FavoritesList

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        return Favoritos.objects.filter(user=user)


class CreateFavorite(CreateAPIView):
    serializer_class = FavoritosSerializer


class DeleteFavorite(DestroyAPIView):
    serializer_class = FavoritosSerializer
    queryset = Favoritos.objects.all()


class UserHasThisFavorite(APIView):
    def post(self, request):
        serializer = FavoritosSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            existe_favorito = Favoritos.objects.get(
                user=serializer.validated_data["user"],
                tienda=serializer.validated_data["tienda"],
            )
        except Favoritos.DoesNotExist:
            existe_favorito = None

        res_dict = {
            "msj": "",
            "id": 0,
        }

        if existe_favorito != None:
            res_dict["msj"] = "exists"
            res_dict["id"] = existe_favorito.id
            return Response(res_dict, status=status.HTTP_200_OK)
        else:
            return Response({"msj": "NO exists"}, status=status.HTTP_200_OK)


class CreateQrCode(CreateAPIView):
    serializer_class = CreateQrSerializer


class GetQrCode(ListAPIView):
    serializer_class = GetQrSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Codigoqr.objects.filter(tienda=tienda)


class ExisteGeolocation(APIView):
    def post(self, request):

        resp = {
            "id": "",
            "mensaje": "",
            "point": "",
            "pais": "",
            "region": "",
            "subregion": "",
            "ciudad": "",
            "direccion": "",
            "codigo_postal": "",
        }

        serializer = GeoDjangoSerializerExists(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]

        existe_credencial = Geolocalization_geodjango.objects.filter(tienda=tienda)

        if existe_credencial.exists():
            geo = Geolocalization_geodjango.objects.get(tienda=tienda)
            cadena = str(geo.location)
            resp = {
                "id": geo.id,
                "mensaje:": "Existe Geolocalizacion",
                "point": cadena[17:-1],
                "pais": geo.pais,
                "region": geo.region,
                "subregion": geo.subregion,
                "ciudad": geo.ciudad,
                "direccion": geo.direccion,
                "codigo_postal": geo.codigo_postal,
            }
            print(resp)
            return Response(resp, status=status.HTTP_200_OK)
        else:
            return Response(
                {"mensaje:": "NO existe Geolocalizacion"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CreateGeoDjango(CreateAPIView):
    serializer_class = GeoDjangoSerializer


class SearchTiendaByDescription(ListAPIView):
    serializer_class = GeolocalizationSerializer

    def get_queryset(self):
        lat = self.request.query_params.get("lat", "")
        lng = self.request.query_params.get("lng", "")
        radius = self.request.query_params.get("radius", "")
        description = self.request.query_params.get("description", "")
        print(lat)
        print(lng)

        point = Point(float(lng), float(lat))

        return Geolocalization_geodjango.objects.filter(
            location__distance_lt=(point, Distance(km=radius)),
            tienda__description__unaccent__trigram_similar=description,
        )


class UpdateGeolocalization(UpdateAPIView):
    serializer_class = GeolocalizationUpdateSerializer
    queryset = Geolocalization_geodjango.objects.all()


class SearchTiendaTriagram(ListAPIView):

    serializer_class = GeolocalizationSerializer

    def get_queryset(self):
        lat = self.request.query_params.get("lat", "")
        lng = self.request.query_params.get("lng", "")
        radius = self.request.query_params.get("radius", "")
        title = self.request.query_params.get("title", "")
        print(lat)
        print(lng)

        point = Point(float(lng), float(lat))

        return Geolocalization_geodjango.objects.filter(
            location__distance_lt=(point, Distance(km=radius)),
            tienda__title__unaccent__trigram_similar=title,
        )


class GeoDjangoNewsStoresNears(ListAPIView):

    serializer_class = GeolocalizationSerializer

    def get_queryset(self):
        lat = self.request.query_params.get("lat", "")
        lng = self.request.query_params.get("lng", "")
        radius = self.request.query_params.get("radius", "")

        point = Point(float(lng), float(lat))

        return Geolocalization_geodjango.objects.filter(
            location__distance_lt=(point, Distance(km=radius)),
        ).order_by("-created_at")


""" NO GeoDjango """


class SearchFilterByLocation(ListAPIView):
    serializer_class = SearchByCitySerializer

    def get_queryset(self):
        criterio = self.request.query_params.get("criterio")
        by = self.request.query_params.get("by")
        kword = self.request.query_params.get("kword")
        pais = self.request.query_params.get("pais")
        region = self.request.query_params.get("region")
        subregion = self.request.query_params.get("subregion")
        ciudad = self.request.query_params.get("ciudad")

        """ POR NOMBRE """
        if by == "name":
            if criterio == "ciudad":
                return Geolocalization_geodjango.objects.filter(
                    tienda__title__unaccent__trigram_similar=kword,
                    pais=pais,
                    region=region,
                    subregion=subregion,
                    ciudad=ciudad,
                )

            if criterio == "subregion":
                return Geolocalization_geodjango.objects.filter(
                    tienda__title__unaccent__trigram_similar=kword,
                    pais=pais,
                    region=region,
                    subregion=subregion,
                )
            if criterio == "region":
                return Geolocalization_geodjango.objects.filter(
                    tienda__title__unaccent__trigram_similar=kword,
                    pais=pais,
                    region=region,
                )
            if criterio == "pais":
                return Geolocalization_geodjango.objects.filter(
                    tienda__title__unaccent__trigram_similar=kword,
                    pais=pais,
                )

        """ POR KEYWORDS """
        if by == "keywords":
            if criterio == "ciudad":
                return Geolocalization_geodjango.objects.filter(
                    tienda__description__unaccent__trigram_similar=kword,
                    pais=pais,
                    region=region,
                    subregion=subregion,
                    ciudad=ciudad,
                )

            if criterio == "subregion":
                return Geolocalization_geodjango.objects.filter(
                    tienda__description__unaccent__trigram_similar=kword,
                    pais=pais,
                    region=region,
                    subregion=subregion,
                )
            if criterio == "region":
                return Geolocalization_geodjango.objects.filter(
                    tienda__description__unaccent__trigram_similar=kword,
                    pais=pais,
                    region=region,
                )

            if criterio == "pais":
                return Geolocalization_geodjango.objects.filter(
                    tienda__description__unaccent__trigram_similar=kword,
                    pais=pais,
                )


class FilterCitiesBySubregion(ListAPIView):
    serializer_class = FilterCitiesBySubregionSerializer

    def get_queryset(self):
        subregion = self.request.query_params.get("subregion")

        return (
            Geolocalization_geodjango.objects.filter(subregion=subregion)
            .values("ciudad")
            .distinct()
        )


class FilterDepartamentosByRegion(ListAPIView):
    serializer_class = FilterDepartamentosByRegionSerializer

    def get_queryset(self):
        region = self.request.query_params.get("region")

        return (
            Geolocalization_geodjango.objects.filter(region=region)
            .values("subregion")
            .distinct()
        )


""" BUSQUEDAS GLOBALES """


class SearchGlobalStoreByTitle(ListAPIView):
    serializer_class = SearchStoreByTitleGlobalSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword")

        return Tienda.objects.filter(title__unaccent__trigram_similar=kword)


class SearchGlobalStoreByDescription(ListAPIView):
    serializer_class = SearchStoreByTitleGlobalSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword")

        return Tienda.objects.filter(description__unaccent__trigram_similar=kword)


class GetTiendasDestacadas(ListAPIView):
    serializer_class = TiendaDestacadaSerializer

    def get_queryset(self):
        pais = self.request.query_params.get("pais")
        region = self.request.query_params.get("region")
        subregion = self.request.query_params.get("subregion")
        ciudad = self.request.query_params.get("ciudad")
        return Tienda.objects.filter(
            extra_field="vip", geo_tienda__ciudad=ciudad
        ).order_by("-created")

class GetTiendasDemo(ListAPIView):
    serializer_class = TiendaDemoSerializer

    def get_queryset(self):
        return Tienda.objects.filter(
            extra_field="vip"
        ).order_by("-created")




class TiendaTitleFont(ListAPIView):
    serializer_class = TitleFrontColorSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda")

        return Colors.objects.filter(tienda=tienda)


""" VISITOR """


class CreateTiendaVisitor(APIView):
    serializer_class = TiendaVisitorCreateSerializer

    def post(self, request, *args, **kwargs):

        serializer = TiendaVisitorCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        visitor = serializer.validated_data["visitor"]
        tienda = serializer.validated_data["tienda"]

        print("visitor")
        print(visitor)
        print("tienda")
        print(tienda)

        existe_tiendavisitor = TiendaVisitor.objects.filter(
            visitor=visitor, tienda=tienda
        )
        if existe_tiendavisitor.exists():
            return Response({"msj": "exists"}, status=HTTP_200_OK)
        else:
            TiendaVisitor.objects.create(visitor=visitor, tienda=tienda)
            return Response({"msj": "success"}, status=HTTP_200_OK)


class GetTiendaVisitor(ListAPIView):
    serializer_class = TiendaVisitorGetSerializer

    def get_queryset(self):
        visitor = self.request.query_params.get("visitor")
        return TiendaVisitor.objects.filter(visitor=visitor).order_by("-created")


""" opiniones """


class CreateOpinion(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        serializer = OpinionCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        tienda_request = serializer.validated_data["tienda"]

        print(user)

        existe_opinion = Opiniones.objects.filter(user=user, tienda=tienda_request)

        if existe_opinion.exists():

            return Response({"msj": "Ya ha comentado"}, status=HTTP_200_OK)

        else:
            Opiniones.objects.create(
                tienda=tienda_request,
                user=user,
                rating=serializer.validated_data["rating"],
                opinion=serializer.validated_data["opinion"],
            )

            return Response({"msj": "Comentario Creado!"}, status=HTTP_200_OK)


class GetOpinionesDeTinda(ListAPIView):
    serializer_class = OpinionListSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda")

        return Opiniones.objects.filter(tienda=tienda).order_by("created")


class PromedioTienda(APIView):
    def get(self, request, *args, **kwargs):
        tienda = self.request.query_params.get("tienda")

        print(tienda)

        averange = Opiniones.objects.filter(tienda=tienda).aggregate(Avg("rating"))
        print("averange")
        print(averange)

        return Response(averange, status=HTTP_200_OK)


class GetUserOpinion(ListAPIView):
    serializer_class = OpinionListSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda")
        user = self.request.query_params.get("user")
        return Opiniones.objects.filter(tienda=tienda, user=user)[0:1]


class UpdateUserOpinion(UpdateAPIView):
    serializer_class = UserOpinionUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Opiniones.objects.all()


class UpdatePaymentsMethods(APIView):
    def post(self, request):
        serializer = PaymentMethodsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tienda_request = serializer.validated_data["tienda"]
        only_order_request = serializer.validated_data["only_order"]
        transfer_request = serializer.validated_data["transfer"]
        mercadopago_request = serializer.validated_data["mercadopago"]

        payment_methods = PaymentMethods.objects.filter(tienda=tienda_request)

        if payment_methods.exists():
            payment_methods.update(
                only_order=only_order_request,
                transfer=transfer_request,
                mercadopago=mercadopago_request,
            )
            print("payment_db")
            print(payment_methods)
            return Response({"msj": "Updated"}, status=HTTP_200_OK)
        else:
            return Response({"msj": "Error"}, status=HTTP_400_BAD_REQUEST)
