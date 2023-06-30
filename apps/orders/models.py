from django.db import models
from django.db.models.expressions import F
from django.db.models.fields import DecimalField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey
from model_utils.models import TimeStampedModel
##Apps local
from apps.tiendas.models import Tienda
from apps.tiendas.models import Envios
from apps.users.models import User,UserPersonalData
from apps.products.models import Product
from .managers import OrderDetailManager,OrderManager
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.contrib.postgres.fields import ArrayField
from .utils import code_generator

# Create your models here.
class AnonymousPersonalData(TimeStampedModel):
    nombre = models.CharField("Nombre",max_length=50,blank=True,null=True)
    apellido = models.CharField("apellido",max_length=50,blank=True,null=True)
    email = models.CharField("email",max_length=100,blank=True,null=True)
    pais = models.CharField("pais",max_length=50,blank=True,null=True)
    ciudad = models.CharField("ciudad",max_length=50,blank=True,null=True)
    estado = models.CharField("estado/provincia",max_length=50,blank=True,null=True)
    direccion = models.CharField("direccion",max_length=80,blank=True,null=True)
    apartamento = models.CharField("apartamento",max_length=10,blank=True,null=True)
    codigo_postal = models.CharField("codigo postal",max_length=50,blank=True,null=True)
    telefono = models.CharField("telefono",max_length=50,blank=True,null=True)
    dni = models.CharField("telefono",max_length=50,blank=True,null=True)


    class Meta:
        verbose_name = "anonymous user data"
        verbose_name_plural = "anonymous user data"

    def __str__(self):
        return str(self.id)+'_'+ str(self.email) + '_' + self.nombre + '_' + self.apellido




class Order(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="Tienda",
        on_delete=models.CASCADE
    )
    user = ForeignKey(
        User,
        related_name='Usuario',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    personal_user_data = models.ForeignKey(
        UserPersonalData,
        verbose_name="Datos Personales",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    anonymous_user_data = models.ForeignKey(
        AnonymousPersonalData,
        verbose_name="anonymous_user_data",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    envio = models.ForeignKey(
        Envios,
        verbose_name="Envio",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    notas = models.CharField("Notas",blank=True,null=True,max_length=255)
    total = models.DecimalField("Total",max_digits=10,decimal_places=2)
    estado = models.CharField("estado",max_length=20,default="en espera")
    metodo_pago = models.CharField("Metodo de pago",max_length=20,default="efectivo")
    quantity_products = PositiveIntegerField('cantidad de productos')
    visto = models.BooleanField('visto',default=False)
    mercado_pago_approved=models.BooleanField('mercado_pago_approved',default=False)
    pago=models.CharField('pago',max_length=11,default='pendiente')
        
    objects = OrderManager()

    class Meta: 
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self):
        return 'tienda_id: ' + str(self.tienda.id)+' tienda_name: '+str(self.tienda.name)+' Orden_id_ '+str(self.id)

class Order_detail(TimeStampedModel):
    order = ForeignKey(
        Order,
        related_name="Orden",
        on_delete=models.CASCADE,
    )
    product = ForeignKey(
        Product,
        related_name="Producto",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField('cantidad')
    price_sale = models.DecimalField("Precion_venta",max_digits=10,decimal_places=2)
    price_off =  models.DecimalField("Precion_en_oferta",max_digits=10,decimal_places=2,blank=True,null=True)
    variacion_id = models.IntegerField("Variacion_id",null=True,blank=True)
    options = ArrayField(
        models.CharField("opciones", max_length=255), blank=True, null=True
    )

    
    objects=OrderDetailManager()


    class Meta:
        verbose_name = "Orden Detalle"
        verbose_name_plural = "Ordenes Detalles"

    def __str__(self):
        return str(self.order.id) + '_' + str(self.product.title)

class OrderMercadoPagoDetail(TimeStampedModel):

    order = ForeignKey(
        Order,
        verbose_name="Orden_",
        on_delete=models.CASCADE,
        related_name='order_mp_detail'
    )
    collection_id = models.CharField('collection_id',max_length=20)
    collection_status = models.CharField('collection_status',max_length=10)
    payment_id = models.CharField('payment_id',max_length=20)
    payment_type = models.CharField('payment_type',max_length=20)
    merchant_order_id = models.CharField('merchant_order_id',max_length=20)
    external_reference = models.CharField('external_reference',max_length=15)

    class Meta:
        verbose_name = "MercadoPago Detalle"
        verbose_name_plural = "MercadoPago Detalles"

    def __str__(self):
        return 'Order_id: '+str(self.order.id) + ' mp_detail_id: ' + str(self.id)


class Ticket(TimeStampedModel):
    product = ForeignKey(
        Product,
        related_name="product_evento",
        on_delete=models.CASCADE,
    )
    token = models.CharField("token", max_length=16)
    personal_user_data = models.ForeignKey(
        UserPersonalData,
        verbose_name="Datos Personales",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    anonymous_user_data = models.ForeignKey(
        AnonymousPersonalData,
        verbose_name="anonymous_user_data",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return 'evento: '+str(self.product.title) + ' Token: ' + str(self.token)




