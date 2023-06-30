from django.db.models import fields
from rest_framework import serializers
from django.db.models import Count, Avg

from .models import (
    Service,
    Booking,
    AnonymousPersonalServiceData,
    Category_Service,
    Service_Images,
    OpinionesServices,
    PreguntaService,
    BookingMercadoPagoDetail
)

from apps.users.models import User, UserPersonalData
from apps.tiendas.models import Tienda

class ListCategoriesSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField("get_children_field")

    
    def get_children_field(self, id):
            return Category_Service.objects.filter(parent=id).values('id','name','image')
             
    class Meta:
        model = Category_Service
        fields = ('id','tienda','parent','name','image','children')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Service
        fields = "__all__"


class CategoriesPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Service
        fields = ("name",)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Images
        fields = ("id", "tienda", "service", "image")


class ServicesSerializer(serializers.ModelSerializer):

    category = CategoriesSerializer()
    images_services = ImageSerializer(many=True)

    class Meta:
        model = Service
        fields = "__all__"


class ServicesDetailSerializer(serializers.ModelSerializer):

    category = CategoriesSerializer()
    images_services = ImageSerializer(many=True)
    average= serializers.SerializerMethodField('get_average_field')
    count_opinion= serializers.SerializerMethodField('get_count_opinion_field')

    def get_average_field(self, id):
        return OpinionesServices.objects.filter(service=id).aggregate(Avg("rating"))

    def get_count_opinion_field(self, id):
        return OpinionesServices.objects.filter(service=id).aggregate(Count("opinion"))

    class Meta:
        model = Service
        fields = (
            "id",
            "images_services",
            "average",
            "count_opinion",
            "category",
            "tienda",
            "image",
            "title",
            "description",
            "public",
            "portada",
            "price",
            "start_time",
            "end_time",
            "interval",
            "color",
            "days",
            "has_break",
            "times_break",
            "booking",
            "payment",
            "payment_price"
        )


class ServicesPublicSerializer(serializers.ModelSerializer):

    category = CategoriesPublicSerializer()

    class Meta:
        model = Service
        fields = (
            "id",
            "image",
            "title",
            "description",
            "category",
        )


class CreateServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServiceBreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("has_break", "times_break")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "service",
            "user_personal_data",
            "anonymous_personal_service_data",
            "date",
            "time",
            "visto",
            "completed"
        )


class CreateBookingSerializer(serializers.ModelSerializer):

    tienda = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = (
            "id",
            "service",
            "user_personal_data",
            "anonymous_personal_service_data",
            "date",
            "time",
            "visto",
            "tienda",
        )


class AnonymousPersonalServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousPersonalServiceData
        fields = "__all__"


class UserPersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalData
        fields = "__all__"


class UserPersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalData
        fields = ("nombre", "apellido", "telefono")


class BookingSerializerToList(serializers.ModelSerializer):

    service = ServicesSerializer()
    anonymous_personal_service_data = AnonymousPersonalServiceDataSerializer()
    user_personal_data = UserPersonalDataSerializer()

    class Meta:
        model = Booking
        fields = (
            "id",
            "service",
            "user_personal_data",
            "anonymous_personal_service_data",
            "date",
            "time",
            "visto",
        )

class MercadoPagoSerializer(serializers.Serializer):
    
    tienda_id = serializers.IntegerField()
    tienda= serializers.CharField()
    total = serializers.DecimalField(max_digits=10,decimal_places=2)
    booking = serializers.IntegerField()


class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = (
            "name",
            "title",
        )


class ServiceForUserSerializer(serializers.ModelSerializer):

    tienda = TiendaSerializer()

    class Meta:
        model = Service
        fields = ("title", "description", "tienda")


class BookingSerializerForUser(serializers.ModelSerializer):

    service = ServiceForUserSerializer()

    class Meta:
        model = Booking
        fields = (
            "id",
            "service",
            "date",
            "time",
            "visto",
        )


class ServiceAndApoimentsSerializer(serializers.ModelSerializer):

    booking_service = serializers.SerializerMethodField()

    def get_booking_service(self,service):
        qs = Booking.objects.filter(service=service, completed=True)
        serializer=BookingSerializer(instance=qs,many=True)
        return serializer.data

    class Meta:
        model = Service
        fields = "__all__"


class UpdateBookingVisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("visto",)

class UpdateBookingCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("completed",)


class ClearBookingsNoVistasSerializer(serializers.Serializer):
    tienda_id = serializers.IntegerField()

class BookingMercadoPagoDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookingMercadoPagoDetail
        fields = ('__all__')


class OnlyTiendaIdSerializer(serializers.Serializer):

    tienda = serializers.IntegerField()


class CategoriesSerializerPrivate(serializers.ModelSerializer):
    class Meta:
        model = Category_Service
        fields = "__all__"


class ServicesSerializerPrivate(serializers.ModelSerializer):

    category = CategoriesSerializerPrivate()

    class Meta:
        model = Service
        fields = "__all__"


class UpdatePublicStatusService(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "tienda",
            "public",
        )


class UpdateService(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "tienda",
            "title",
            "description",
            "public",
            "portada",
            "price",
            "start_time",
            "end_time",
            "interval",
            "color",
        )


class PortadaServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("image",)

""" opiniones """

class OpinionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OpinionesServices
        fields = (
            "service",
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
        model = OpinionesServices
        fields = (
            "id",
            "user",
            "service",
            "rating",
            "opinion",
            "created"
            )

class UserOpinionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpinionesServices
        fields = ("rating","opinion")


""" opiniones """

###preguntas

class PreguntaServiceSerializer(serializers.ModelSerializer):

    user = UserOpinionSerializaer()

    class Meta:
        model = PreguntaService
        fields = (
            "id",
            "service",
            "user",
            "pregunta",
            "respuesta",
            "visto",
            "created",
            "modified"
            )

class PreguntaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreguntaService
        fields = (
            "service",
            "pregunta",
            )

class ServiceToPreguntaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = (
            "title",
            "description",
            "image",
        )


class PreguntaServiceAdminSerializer(serializers.ModelSerializer):

    user = UserOpinionSerializaer()
    service = ServiceToPreguntaSerializer()
    

    class Meta:
        model = PreguntaService
        fields = (
            "id",
            "service",
            "user",
            "pregunta",
            "respuesta",
            "visto",
            "created",
            "modified"
            )


class PreguntaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreguntaService
        fields = (
            "respuesta",
            "visto"
        )

class ClearServiceQuestionsNoVistasSerializer(serializers.Serializer):
    tienda = serializers.IntegerField()