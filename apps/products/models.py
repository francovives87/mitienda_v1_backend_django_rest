from email.policy import default
from django.db import models
#Apps terceros
from model_utils.models import TimeStampedModel
##Apps local
from apps.tiendas.models import Tienda
from apps.users.models import User
from PIL import Image
#Manager
from .managers import (
    ProductManager,
    CategoryManager,
    AtributoManager
)


#Models

class Category(TimeStampedModel):
    """ Modelo para categorias """
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda_category",
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE, blank=True,null=True)
    name = models.CharField('Nombre', max_length=40)
    image = models.ImageField(
        "Imagen", 
        upload_to="category_product", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True,
        )
    
    def save(self, *args, **kwargs):
        instance = super(Category, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((640,480))
        images.save(self.image.path,quality=50,optimize=True)
        return instance

    objects=CategoryManager()

    class Meta:
        verbose_name = "Categoria Producto"
        verbose_name_plural = "Categorias Productos"

    def __str__(self):
        return 'tienda_id: '+str(self.tienda.id) + ' tienda_nombre: '+str(self.tienda.name)+' categoria_id: '+str(self.id)+' name: '+str(self.name)

class Product(TimeStampedModel):
    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda_product",
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, 
        verbose_name="Categoria", 
        on_delete=models.CASCADE
        )
    marca = models.CharField("Marca del producto",max_length=100, blank=True,null=True)
    title = models.CharField("Titulo", max_length=200)
    description = models.TextField("Descripcion:")
    public = models.BooleanField("publico",default=False)
    image = models.ImageField(
        "Imagen", 
        upload_to="products", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        null=True,
        blank=True,
        )
    price = models.DecimalField("Precio", max_digits=8, decimal_places=2, blank=True,null=True)
    portada = models.BooleanField("Destacado",default=False)
    in_offer = models.BooleanField("En oferta",default=False)
    in_offer_price = models.DecimalField("Precio de oferta", max_digits=8, decimal_places=2,null=True,blank=True)
    has_variation = models.BooleanField("Variaciones",default=False)
    has_options = models.BooleanField("con opciones",default=False)
    stock = models.IntegerField("stock",null=True,blank=True)
    no_stock= models.BooleanField("no_stock",default=False)
    only_attribute= models.BooleanField("only_attribute",default=True)
    type = models.CharField("Tipo", max_length=3, default="pdf")
    visits = models.IntegerField("visitas", default=0)

    
    def save(self, *args, **kwargs):
        instance = super(Product, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((640,480))
        images.save(self.image.path,quality=50,optimize=True)
        return instance

    objects = ProductManager()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return 'tienda_id:'+ str(self.tienda.id)+' tienda_nombre: '+str(self.tienda.name)+ ' producto_id: ' +  str(self.id)+' producto_nombre: '+ self.title + ' in_offer ' + str(self.in_offer)


class Images(TimeStampedModel):
    product= models.ForeignKey(
        Product,
        verbose_name='producto',
        on_delete=models.CASCADE,
        related_name='images_product',
    )
    image = models.ImageField(
        "Image", 
        upload_to="product_more_images", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        )
    tienda= models.ForeignKey(
        Tienda,
        verbose_name='tienda',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        instance = super(Images, self).save(*args, **kwargs)
        images = Image.open(self.image.path)
        images = images.resize((640,480))
        images.save(self.image.path,quality=50,optimize=True)
        return instance
 
    
    
    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Mas Imagenes de los productos"

    def __str__(self):
        return 'product_id: '+ str(self.product.id)+' product_name: '+str(self.product.title)+' image_id: '+str(self.id)  +' image: ' + self.image.url


class Atributos(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="Producto", 
        on_delete=models.CASCADE
    )
    nombre = models.CharField("Nombre",max_length=150)
    repeat= models.IntegerField("Repetir",default=0)
    

    objects = AtributoManager()

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"

    def __str__(self):
        return 'product_id :' +str(self.product.id)+' product_name: '+str(self.product.title) + ' atributo_id: '+ str(self.id)+' atributo_name: '+ self.nombre


class Atributos_Items(TimeStampedModel):
    atributo = models.ForeignKey(
        Atributos,
        verbose_name="Atributo", 
        on_delete=models.CASCADE,
        related_name='atributo_item'
    )
    item = models.CharField("Item",max_length=150)

    class Meta:
        verbose_name = "Atributo_Item"
        verbose_name_plural = "Atributos_Items"

    def __str__(self):
        return str(self.atributo.id)+'__'+str(self.atributo.nombre)+'__'+str(self.id)+'__'+ self.item

class Variaciones(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="Producto", 
        on_delete=models.CASCADE
    )
    item = models.ManyToManyField(Atributos_Items)
    stock = models.IntegerField(blank=True,null=True)
    price = models.DecimalField("Precio", max_digits=8, decimal_places=2, blank=True,null=True)
    no_stock = models.BooleanField("no_stock",default=False)
    class Meta:
        verbose_name = "Variacion"
        verbose_name_plural = "Variaciones"

    def __str__(self):
        return 'Id_Producto: '+str(self.product.id)+'__'+' Id_variacion: '+str(self.id)


class OpinionesProducts(TimeStampedModel):
    product = models.ForeignKey(
        Product,
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
        verbose_name = "Opinion Producto"
        verbose_name_plural = "Opiniones Productos"

    def __str__(self):
        return  "opinion_id: "+str(self.id)+" product_id "+ str(self.product.id) + ' product_name ' +str(self.product.title) + ' user '+str(self.user.username)+ ' rating '+str(self.rating)


class PreguntaProduct(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        verbose_name="producto",
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
        return "id_pregunta" + str(self.id) + " product_id: " +str(self.product.id)+" product_name: "+str(self.product.title) + " user_id :"+ str(self.user.id)+ " username: "+str(self.user.username) +" pregunta: "+str(self.pregunta)


