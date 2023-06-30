from model_utils.models import TimeStampedModel
from apps.users.models import User,Visitor
from .managers import TiendaManager,SliderManager,ColorsManager
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


# Create your models here.


class Plan(TimeStampedModel):
    name = models.CharField("Nombre",max_length=50)
    product_categories = models.IntegerField("product_categories")
    product_products= models.IntegerField("product_products")
    blog_categories=models.IntegerField("blog_categories")
    blog_entries=models.IntegerField("blog_entries")
    images_x_products=models.IntegerField("imagenes_x_producto")
    images_x_services=models.IntegerField("imagenes_x_servicio")
    images_x_entries=models.IntegerField("imagenes_x_entrada")
    images_sliders=models.IntegerField("imagenes_sliders")
    services_categories = models.IntegerField("servicios_categorias")
    services=models.IntegerField("servicios")
    orders=models.IntegerField("ordenes")
    bookings=models.IntegerField("reservas")
    

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

    
    def __str__(self):
        return 'id_plan: '+str(self.id)+' nombre: '+ self.name + ' ' + 'product_categories: '+str(self.product_categories) + 'product_products' + str(self.product_products) + 'blog_categories' + str(self.blog_categories) +'blog_entries' + str(self.blog_entries)+'images_x_products' + str(self.images_x_products)+'images_x_entries'+str(self.images_x_entries)


class Tienda(TimeStampedModel):
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(
        Plan,
        verbose_name="Plan",
        on_delete=models.CASCADE,
        default=1,
        related_name="tienda_plan"
    )
    name = models.CharField('dominio',max_length=30,unique=True)
    title= models.CharField('titulo',max_length=30)
    description = models.CharField('Descripcion',max_length=255)
    logo =  models.ImageField("logo", 
        upload_to='logo', 
        height_field=None, 
        width_field=None, 
        max_length=None,
        null=True,
        blank=True,
        default='/defaults/logo_generico.png'
        )
    tipo_tienda = models.IntegerField("tipo_tienda",default=1)
    extra_field = models.CharField("extra_field",max_length=4,blank=True,null=True)
    visits = models.IntegerField("visitas", default=0)
    
    objects = TiendaManager()


    class Meta:
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'

    
    def __str__(self):
        return 'id_tienda: '+str(self.id)+' nombre: '+ self.name+'||'+'plan' + str(self.plan.id)



class TiendaVisitor(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE
    )  
    visitor = models.ForeignKey(
        Visitor,
        verbose_name="visitor",
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = "TiendaVisitor"
        verbose_name_plural = "TiendaVisitor"
    
    def __str__(self):
        return "id: "+ str(self.id) +"visitor_id:" + str(self.visitor.id)+ " tienda_id: "+str(self.tienda.id) +" tienda_name: "+str(self.tienda.name)


class Slider(TimeStampedModel):
    """ Modelo para slider """
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE
    )
    image = models.ImageField("Imagen", 
        upload_to='slider', 
        height_field=None, 
        width_field=None, 
        max_length=None
        )
    is_public = models.BooleanField("Publicado")

    def save(self, *args, **kwargs):
        instance = super(Slider, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((1920,1080))
        images.save(self.image.path,quality=50,optimize=True)
        
        return instance

    objects =SliderManager()


    class Meta:
        verbose_name = "Diapositiva"
        verbose_name_plural = "Diapositivas"

    def __str__(self):
        return 'tienda_id:' + str(self.tienda.id) + ' tienda_nane: ' +str(self.tienda.name) + ' slide_id: '+ str(self.id)

class Textures(TimeStampedModel):
    image = models.ImageField("Imagen", 
    upload_to='Textures', 
    height_field=None, 
    width_field=None, 
    max_length=None
    )

    class Meta:
        verbose_name = "Textura"
        verbose_name_plural = "Texturas"

    def __str__(self):
        return str(self.id)+'__/'+ str(self.image.name)

class Title_font(TimeStampedModel):
    name = models.CharField("nombre",max_length=20, unique=True)
    url= models.CharField("url",max_length=200)
    css = models.CharField("css",max_length=100)
    
    class Meta:
        verbose_name = "fuente_titulo"
        verbose_name_plural = "fuentes titulo"

    def __str__(self):
        return ' title_font_id: '+str(self.id) + ' font_name: ' + str(self.name)


class Colors(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name='tienda',
        on_delete=models.CASCADE,
        related_name='tienda_colors'
    )
    font_title = models.ForeignKey(
        Title_font,
        verbose_name='fuente_titulo',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=1
    )
    font_title_size= models.IntegerField("Tamaño de la fuente",default=30,validators=[MinValueValidator(10), MaxValueValidator(60)] )
    navbar = models.CharField("navbar",max_length=15,default='#A463BF')
    navbar_font = models.CharField("navbar_font",max_length=15,null=True,blank=True,default="#ffffff")
    bottom_navigation = models.CharField("bottom_navigation",max_length=15,default='#A463BF')
    bottom_navigation_font = models.BooleanField("bottom_navigation_font",default=True)
    alerts = models.CharField("alerts",max_length=15,null=True,blank=True,default="#A463BF")
    alerts_font = models.CharField("alerts_fonts",max_length=15,null=True,blank=True,default="#ffffff")
    background_color = models.CharField('background_color',max_length=15,blank=True,null=True, default='#FFFFFF')
    hasTexture = models.BooleanField("hasTexture",default=True)
    texture = models.ForeignKey(
        Textures,
        verbose_name='fondo_textura',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=15
    )
    info_background_color=models.CharField('info_background_color',max_length=15,blank=True,null=True, default='#9c06a8')
    info_icons_color=models.CharField('info_icons_color',max_length=15,blank=True,null=True, default='#FFFFFF')
    info_font_color=models.CharField('info_font_color',max_length=15,blank=True,null=True, default='#FFFFFF')
    
    objects = ColorsManager()

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"

    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id)+' tienda_name: '+str(self.tienda.name)+' colors_id: '+str(self.id)



class Informacion(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="tienda_informacion"
    )
    dias_horarios= models.TextField("horario",blank=True,null=True,default='Lunes a Viernes De 09:00 a 13:00 y 15:00 a 19:00,<br> Sabado de 09:00 a 13:00')
    telefono=models.CharField("telefono",max_length=100,blank=True,null=True,default="54 9 3415 666777")
    whatsapp=models.CharField("whatsapp",max_length=30,blank=True,null=True)

    class Meta:
        verbose_name = "Informacion"
        verbose_name_plural = "Informacion"

    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id)+' tienda_name: '+str(self.tienda.name)+' informacion_id: '+str(self.id)


class MercadoPago(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="tienda_mercadopago"
    )
    public_key= models.CharField("public_key",max_length=150)
    access_token= models.CharField("access_token",max_length=150)

    class Meta:
        verbose_name = "MercadoPago"
        verbose_name_plural = "MercadoPago"

    def __str__(self):
        return 'tienda_id: ' + str(self.tienda.id)+' tienda_name: ' + str(self.tienda.name) + 'mp_id: ' + str(self.id)+' public_key ' + str(self.public_key) + ' access_token ' + str(self.access_token)

class Envios(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="tienda_envios"
    )
    name=models.CharField("nombre",max_length=100)
    description=models.TextField('description')
    price=models.DecimalField("Precio", max_digits=8, decimal_places=2, blank=True,null=True)

    class Meta:
        verbose_name = "envio"
        verbose_name_plural = "envios"
    
    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id)+' ' +'envio_id: '+str(self.id)+' '+'name: '+str(self.name)

class Favoritos(TimeStampedModel):
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE
    )
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
    
    def __str__(self):
        return "favo_id: "+ str(self.id) +"user_id:" + str(self.user.id)+ " username: "+str(self.user.username) +" tienda_id: "+str(self.tienda.id) + " tienda_name: " +str(self.tienda.name)


class Codigoqr(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="qr_code"
    )
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make('https://mitienda.app/'+self.tienda.name)
        canvas = Image.new('RGB',(360,360),'white')
        
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.tienda.name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args,**kwargs)
    
    
    class Meta:
        verbose_name = "Codigo QR"
        verbose_name_plural = "Codigos QR"
    
    def __str__(self):
        return  str(self.id) + ' ' +str(self.tienda.name)

class Geolocalization_geodjango(models.Model):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="geo_tienda"
    )
    pais= models.CharField("pais",max_length=150, blank=True ,null=True)
    region= models.CharField("region",max_length=150, blank=True ,null=True)
    subregion= models.CharField("subregion",max_length=150, blank=True ,null=True)
    ciudad= models.CharField("ciudad",max_length=150, blank=True ,null=True)
    direccion= models.CharField("direccion",max_length=150, blank=True ,null=True)
    codigo_postal= models.CharField("codigo_postal",max_length=150, blank=True ,null=True)
    barrio= models.CharField("barrio",max_length=150, blank=True ,null=True)
    location = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  str(self.tienda.name)

    class Meta:
        verbose_name = "Geolozalizacion_geodjango"
        verbose_name_plural = "Geolocalizaciones_geodjango"

    def __str__(self):
        return  str(self.id) + ' ' +str(self.tienda.name)


class Opiniones(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE
    )
    rating= models.DecimalField("Rating", max_digits=2, decimal_places=1, blank=True,null=True)
    opinion=models.CharField(max_length=255,blank=True,null=True)
    
    class Meta:
        verbose_name = "Opinion"
        verbose_name_plural = "Opiniones"

    def __str__(self):
        return  "tienda_id "+ str(self.tienda.id) + ' tienda_name ' +str(self.tienda.name) + ' user '+str(self.user.username)+ ' rating '+str(self.rating)

class PaymentMethods(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="payment_methods"
    )
    only_order = models.BooleanField("solo_ordenar", default=False)
    transfer = models.BooleanField("transferencia",default=False)
    mercadopago = models.BooleanField("mercadopago",default=False)
    
    class Meta:
        verbose_name = "Metodo de pago"
        verbose_name_plural = "Metodos de pago"

    def __str__(self):
        return  "tienda_id "+ str(self.tienda.id) + ' tienda_name ' +str(self.tienda.name) + ' [order] => ' +str(self.only_order) + ' [transfer] => ' + str(self.transfer) + ' [mp] => ' +str(self.mercadopago)

class TransferData(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda",
        on_delete=models.CASCADE,
        related_name="transfer_data"
    )
    bank = models.CharField("banco", max_length=50)
    alias = models.CharField("alias",max_length=100,blank=True,null=True)
    cbu = models.CharField("cbu",max_length=100)
    
    class Meta:
        verbose_name = "Data de transferencia"
        verbose_name_plural = "Data de transferencia"

    def __str__(self):
        return  "tienda_id "+ str(self.tienda.id) + ' tienda_name ' +str(self.tienda.name) + ' [bank] => ' +str(self.bank) + ' [alias] => ' + str(self.alias) + ' [cbu] => ' +str(self.cbu)
