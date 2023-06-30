from django.db.models import fields
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from rest_framework_gis.serializers import GeometryField
from django.db.models import Count, Avg
from apps.users.models import User
from django.db.models import Func

from .models import (
    Envios,
    Plan,
    Tienda,
    Slider,
    Colors,
    Textures,
    Informacion,
    Favoritos,
    Codigoqr,
    Geolocalization_geodjango,
    TiendaVisitor,
    Opiniones,
    Title_font,
    PaymentMethods,
    TransferData
)

class TransferDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferData
        fields = ("__all__")

class PaymentMethodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethods
        fields = (
            "only_order",
            "transfer",
            "mercadopago"
            )

class TexturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textures
        fields = "__all__"


class TitleFontSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title_font
        fields = ('__all__')

class TitleFrontColorSerializer(serializers.ModelSerializer):

    font_title = TitleFontSerializer()
    
    class Meta:
        model = Colors
        fields = ('font_title','tienda')


class TitleFontUpdate(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('font_title','font_title_size')

class ColorsSerializer(serializers.ModelSerializer):

    texture = TexturesSerializer(required=False)
    font_title = TitleFontSerializer(required=False)

    class Meta:
        model = Colors
        fields = (
            "id",
            "tienda",
            "navbar",
            "navbar_font",
            "bottom_navigation",
            "bottom_navigation_font",
            "alerts",
            "alerts_font",
            "background_color",
            "hasTexture",
            "texture",
            "info_background_color",
            "info_icons_color",
            "info_font_color",
            "font_title",
            "font_title_size"
        )


class InformacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informacion
        fields = "__all__"


class PlanTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class GeoTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        fields = ("pais", "region", "subregion", "ciudad", "direccion", "barrio")

class TiendaQrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigoqr
        fields = ("qr_code",)

class TiendaSerializer(serializers.ModelSerializer):

    tienda_colors = ColorsSerializer(many=True)
    tienda_informacion = InformacionSerializer(many=True)
    plan = PlanTiendaSerializer()
    geo_tienda = GeoTiendaSerializer(many=True)
    qr_code = TiendaQrSerializer(many=True)
    """ ejemplo de como agregar una funcion a un modelSerializer """
    """ en este caso, calcular el promedio de opiniones """
    average= serializers.SerializerMethodField('get_average_field')
    payment_methods = PaymentMethodsSerializer(many=True)
    transfer_data=TransferDataSerializer(many=True)

    def get_average_field(self,id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate((Avg('rating')))

    class Meta:
        model = Tienda
        fields = (
            "id",
            "user",
            "plan",
            "name",
            "description",
            "tienda_colors",
            "logo",
            "title",
            "tienda_informacion",
            "tipo_tienda",
            "geo_tienda",
            "average",
            "qr_code",
            "payment_methods",
            "transfer_data"
        )


class TiendaDestacadaSerializer(serializers.ModelSerializer):

    geo_tienda = GeoTiendaSerializer(many=True)

    average= serializers.SerializerMethodField('get_average_field')

    def get_average_field(self,id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate((Avg('rating')))


    class Meta:
        model = Tienda
        fields = (
            "name",
            "description",
            "logo",
            "title",
            "geo_tienda",
            "average"
        )

class TiendaDemoSerializer(serializers.ModelSerializer):

    geo_tienda = GeoTiendaSerializer(many=True)
    average= serializers.SerializerMethodField('get_average_field')

    def get_average_field(self,id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate((Avg('rating')))


    class Meta:
        model = Tienda
        fields = (
            "name",
            "description",
            "logo",
            "title",
            "geo_tienda",
            "average"
        )


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ("image", "is_public")


class UpdateColorsTextureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = "__all__"


class UpdateTiendaLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = (
            "id",
            "logo",
        )


class UpdateTiendaTituloSerializer(serializers.Serializer):

    tienda = serializers.IntegerField()
    title = serializers.CharField()


class SliderPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = "__all__"


class SliderPublicUptade(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ("is_public",)


class CreateTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ("name", "title", "description")


class MercadoPagoCredentialExists(serializers.Serializer):

    tienda = serializers.IntegerField()

class TransferCredentialExists(serializers.Serializer):

    tienda = serializers.IntegerField()

class TransferDataCredentials(serializers.Serializer):

    tienda = serializers.IntegerField()
    bank = serializers.CharField()
    alias = serializers.CharField()
    cbu = serializers.CharField()


class MercadoPagoCredential(serializers.Serializer):

    tienda = serializers.IntegerField()
    public_key = serializers.CharField()
    access_token = serializers.CharField()


class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envios
        fields = "__all__"


class UserHasTiendaSerializer(serializers.Serializer):

    user_id = serializers.IntegerField()


class TiendaSearchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tienda
        fields = ("id", "name", "title", "description", "logo")


class TipoDeTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = ("tipo_tienda",)


class FavoritosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoritos
        fields = "__all__"


class FavoritesList(serializers.ModelSerializer):

    tienda = TiendaSearchSerializer()

    class Meta:
        model = Favoritos
        fields = ("user", "tienda")


class CreateQrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigoqr
        fields = ("tienda",)


class GetQrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigoqr
        fields = "__all__"


class SeriealizerGenericoParaTiendaOnly(serializers.Serializer):

    tienda = serializers.IntegerField()


class TiendaToSearch(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = "__all__"


class GeoDjangoSerializer(GeoModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        geo_field = "location"
        fields = "__all__"


class GeoDjangoSerializerExists(GeoModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        fields = ("tienda",)


class GeoDjangoGetNearStoresSerializer(serializers.Serializer):

    lng = serializers.FloatField()
    lat = serializers.FloatField()
    radius = serializers.IntegerField()


class GeoDjangoSearchByDescriptionSerializer(serializers.Serializer):

    lng = serializers.FloatField()
    lat = serializers.FloatField()
    radius = serializers.IntegerField()
    description = serializers.CharField()


class GeoDjangoSearchByTitleSerializer(serializers.Serializer):

    lng = serializers.FloatField()
    lat = serializers.FloatField()
    radius = serializers.IntegerField()
    title = serializers.CharField()


class GeoDjangoGetNewsStoresNear(serializers.Serializer):

    lng = serializers.FloatField()
    lat = serializers.FloatField()
    radius = serializers.IntegerField()


""" serializadores para busquedas sin GeoDjango """


class TiendaSerializerToSeachrs(serializers.ModelSerializer):


    average= serializers.SerializerMethodField('get_average_field')

    def get_average_field(self,id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate(Avg('rating'))

    class Meta:
        model = Tienda
        fields = (
            "name",
            "title",
            "logo",
            "description",
            "average"
        )


class SearchByCitySerializer(GeoModelSerializer):

    tienda = TiendaSerializerToSeachrs()

    class Meta:
        model = Geolocalization_geodjango
        geo_field = "location"
        fields = ("tienda", "pais", "region", "subregion", "ciudad", "direccion")


class FilterCitiesBySubregionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        geo_field = "location"
        fields = ("ciudad",)


class FilterDepartamentosByRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        geo_field = "location"
        fields = ("subregion",)


""" Busquedas globales """


class GeolocalizationForGlobarSerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        fields = ("pais", "region", "subregion", "ciudad", "direccion")


class SearchStoreByTitleGlobalSerializer(serializers.ModelSerializer):

    geo_tienda = GeolocalizationForGlobarSerchSerializer(many=True)
    average= serializers.SerializerMethodField('get_average_field')

    def get_average_field(self,id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate(Avg('rating'))

    class Meta:
        model = Tienda
        fields = ("id","name", "title", "description", "logo", "geo_tienda","average")


class GeolocalizationSerializer(GeoModelSerializer):

    tienda = TiendaSerializerToSeachrs()

    class Meta:
        model = Geolocalization_geodjango
        geo_field = "location"
        fields = (
            "tienda",
            "location",
            "pais",
            "region",
            "subregion",
            "ciudad",
            "direccion",
        )


class GeolocalizationUpdateSerializer(GeoModelSerializer):
    class Meta:
        model = Geolocalization_geodjango
        geo_field = "location"
        fields = (
            "location",
            "pais",
            "region",
            "subregion",
            "ciudad",
            "direccion",
        )


""" VISITOR """


class TiendaVisitorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiendaVisitor
        fields = "__all__"


class TiendaToShowVisitorSerializer(serializers.ModelSerializer):

    geo_tienda = GeoTiendaSerializer(many=True)
    average= serializers.SerializerMethodField('get_average_field')

    def get_average_field(self,id):
        return Opiniones.objects.filter(
            tienda=id
        ).aggregate(Avg('rating'))


    class Meta:
        model = Tienda
        fields = ("id", "name", "title", "logo","description", "geo_tienda","average")


class TiendaVisitorGetSerializer(serializers.ModelSerializer):

    tienda = TiendaToShowVisitorSerializer()

    class Meta:
        model = TiendaVisitor
        fields = ("tienda", "visitor")

class OpinionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Opiniones
        fields = (
            "tienda",
            "rating",
            "opinion"
            )

class UserOpinionSerializaer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username",)

class OpinionListSerializer(serializers.ModelSerializer):
    
    user = UserOpinionSerializaer()

    class Meta:
        model = Opiniones
        fields = (
            "id",
            "user",
            "tienda",
            "rating",
            "opinion",
            "created"
            )

class UserOpinionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opiniones
        fields = ("rating","opinion")

class PaymentMethodsUpdateSerializer(serializers.Serializer):
    tienda = serializers.IntegerField(required=True)
    only_order = serializers.BooleanField()
    transfer= serializers.BooleanField()
    mercadopago= serializers.BooleanField()