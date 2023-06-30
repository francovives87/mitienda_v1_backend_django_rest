from pyexpat import model
from django.db import models
from model_utils.models import TimeStampedModel
from apps.tiendas.models import Tienda
from apps.users.models import User, UserPersonalData
from django.contrib.postgres.fields import ArrayField
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from PIL import Image

# Create your models here.


class Category_Service(TimeStampedModel):
    """ Modelo para categorias """
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda_service_category",
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField('Nombre', max_length=40)
    image = models.ImageField(
        "Imagen", 
        upload_to="category_service", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True,
        )

    def save(self, *args, **kwargs):
        instance = super(Category_Service, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((640,480))
        images.save(self.image.path,quality=50,optimize=True)
        return instance

    class Meta:
        verbose_name = "Categoria de servicio"
        verbose_name_plural = "Categorias servicios"

    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id) + ' tienda_nombre: '+str(self.tienda.name)+' categoria_id: '+str(self.id)+' name: '+str(self.name)



class Service(TimeStampedModel):
    
    category = models.ForeignKey(
        Category_Service, 
        verbose_name="Categoria", 
        on_delete=models.CASCADE
        )
    
    tienda = models.ForeignKey(
        Tienda, verbose_name="tienda_service", on_delete=models.CASCADE
    )
    image = models.ImageField(
        "Imagen",
        upload_to="services",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )
    title = models.CharField("Titulo", max_length=200)
    description = models.TextField("Descripcion:")
    public = models.BooleanField("publico", default=False)
    portada = models.BooleanField("Destacado",default=False)
    price = models.DecimalField(
        "Precio", max_digits=8, decimal_places=2, blank=True, null=True
    )
    start_time = models.IntegerField("start_time", default="9")
    end_time = models.IntegerField("end_time", default="20")
    interval = models.IntegerField("interval", default="60")
    color = models.CharField("color", max_length=7, default="#000000")
    days = ArrayField(models.CharField(max_length=20), blank=True)
    has_break = models.BooleanField("has_break", default=False)
    times_break = ArrayField(
        models.CharField("times_break", max_length=100), blank=True, null=True 
    )
    booking = models.BooleanField("booking",default=False)
    payment = models.BooleanField("payment",default=False)
    payment_price = models.DecimalField(
        "payment_price", max_digits=8, decimal_places=2, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        instance = super(Service, self).save(*args, **kwargs)
        if self.image:
            images = Image.open(self.image.path)
            images = images.resize((640,480))
            images.save(self.image.path,quality=50,optimize=True)
            return instance


    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return (
            "tienda_id:"
            + str(self.tienda.id)
            + " tienda_nombre: "
            + str(self.tienda.name)
            + " service_id: "
            + str(self.id)
            + " service_nombre: "
            + self.title
        )


class AnonymousPersonalServiceData(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=50)
    apellido = models.CharField("apellido", max_length=50)
    email = models.CharField("email", max_length=100, blank=True, null=True)
    telefono = models.CharField("telefono", max_length=50)

    class Meta:
        verbose_name = "anonymous user service data"
        verbose_name_plural = "anonymous user service data"

    def __str__(self):
        return (
            str(self.id)
            + "_"
            + str(self.email)
            + "_"
            + self.nombre
            + "_"
            + self.apellido
        )


class Booking(TimeStampedModel):
    service = models.ForeignKey(
        Service,
        verbose_name="booking service",
        related_name="booking_service",
        on_delete=models.CASCADE,
    )
    user_personal_data = models.ForeignKey(
        UserPersonalData,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    anonymous_personal_service_data = models.ForeignKey(
        AnonymousPersonalServiceData,
        verbose_name="anonymous_user_data",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date = models.DateField("fecha")
    time = models.TimeField("hora", auto_now=False, auto_now_add=False)
    visto = models.BooleanField("visto",default=False)
    completed = models.BooleanField("completed",default=False)

    def save(self, *args, **kwargs):
        tienda_id = self.service.tienda.id
        print(tienda_id)
        if self.completed == False:
            return super(Booking,self).save(*args, **kwargs)
        if self.completed == True:
            res = {
                'tienda_id': tienda_id
            }
        print(res)
        if self.visto == False:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'notifi',{
                    'type' : 'send_notifi_booking',
                    'text' : json.dumps(res)
                }
            ) 
        return super(Booking,self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return (
            "service_id:"
            + str(self.service.id)
            + " service_nombre: "
            + str(self.service.title)
            + " booking_id: "
            + str(self.id)
        )


class BookingMercadoPagoDetail(TimeStampedModel):

    booking = models.ForeignKey(
        Booking,
        verbose_name="booking",
        on_delete=models.CASCADE,
        related_name='booking_mp_detail'
    )
    collection_id = models.CharField('collection_id',max_length=20)
    collection_status = models.CharField('collection_status',max_length=10)
    payment_id = models.CharField('payment_id',max_length=20)
    payment_type = models.CharField('payment_type',max_length=20)
    merchant_order_id = models.CharField('merchant_order_id',max_length=20)
    external_reference = models.CharField('external_reference',max_length=15)

    class Meta:
        verbose_name = "Booking MercadoPago Detalle"
        verbose_name_plural = "Bookings MercadoPago Detalles"

    def __str__(self):
        return 'Order_id: '+str(self.order.id) + ' mp_detail_id: ' + str(self.id)


class Service_Images(TimeStampedModel):
    tienda= models.ForeignKey(
        Tienda,
        verbose_name='tienda',
        on_delete=models.CASCADE,
    )
    service= models.ForeignKey(
        Service,
        verbose_name='Servicio',
        on_delete=models.CASCADE,
        related_name='images_services',
    )
    image = models.ImageField(
        "Image", 
        upload_to="service_more_images", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        )
    
    def save(self, *args, **kwargs):
        instance = super(Service_Images, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((640,480))
        images.save(self.image.path,quality=50,optimize=True)
        return instance

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Mas Imagenes de los productos"

    def __str__(self):
        return 'service_id: '+ str(self.service.id)+' service_name: '+str(self.service.title)+' image_id: '+str(self.id)  +' image: ' + self.image.url

class OpinionesServices(TimeStampedModel):
    service = models.ForeignKey(
        Service,
        verbose_name="producto",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    rating= models.DecimalField("Rating", max_digits=2, decimal_places=1, blank=True,null=True)
    opinion=models.CharField(max_length=255,blank=True,null=True)
    
    class Meta:
        verbose_name = "Opinion Servicio"
        verbose_name_plural = "Opiniones Servicios"

    def __str__(self):
        return  "opinion_id: "+str(self.id)+" service_id "+ str(self.service.id) + ' service_name ' +str(self.service.title) + ' user '+str(self.user.username)+ ' rating '+str(self.rating)


class PreguntaService(TimeStampedModel):
    service = models.ForeignKey(
        Service,
        verbose_name="servicio",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    pregunta = models.CharField(max_length=255,blank=True,null=True)
    respuesta = models.CharField(max_length=255,blank=True,null=True)
    visto = models.BooleanField('visto',default=False)

    

    class Meta:
        verbose_name = "Pregunta a vendedor"
        verbose_name_plural = "Pregunta a vendedor"

    def __str__(self):
        return "id_pregunta" + str(self.id) + " service_id: " +str(self.service.id)+" service_name: "+str(self.service.title) + " user_id :"+ str(self.user.id)+ " username: "+str(self.user.username) +" pregunta: "+str(self.pregunta)


