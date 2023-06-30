from django.db import models
#Apps terceros
from model_utils.models import TimeStampedModel
#Apps Local
from apps.tiendas.models import Tienda
from apps.users.models import User

#Manager
from .managers import EntryManager

class Category_blog(TimeStampedModel):
    """ Modelo para categorias """

    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda_blog_category",
        on_delete=models.CASCADE
    )
    name = models.CharField('Nombres', max_length=30)
    
    class Meta:
        verbose_name = "Categoria Blog"
        verbose_name_plural = "Categorias Blog"

    def __str__(self):
         return 'tienda_id: '+str(self.tienda.id) + ' tienda_nombre: '+str(self.tienda.name)+' categoria_id: '+str(self.id)+' name: '+str(self.name)
    

class Tag(TimeStampedModel):
    """ Modelo para etiquetas de un articulo """

    name = models.CharField("Nombre", max_length=30)
    
    class Meta:
        verbose_name = "Etiqueta Blog"
        verbose_name_plural = "Etiquetas Blog"

    def __str__(self):
        return self.name


class Entry(TimeStampedModel):
    """ Modelo para entrada o articulos """

    tienda = models.ForeignKey(
        Tienda,
        verbose_name="tienda_blog_entry",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category_blog, 
        verbose_name="categoria_blog", 
        on_delete=models.CASCADE
        )
    title = models.CharField("Titulo", max_length=200)
    content = models.TextField("Contenido")
    public = models.BooleanField("publico",default=False)
    image = models.ImageField(
        "Imagen", 
        upload_to="entry", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        )
    portada = models.BooleanField("Portada",default=False)
    slug = models.SlugField("Slug",max_length=300,blank=True,null=True)

    objects= EntryManager()

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return 'tienda_id:'+str(self.tienda.id)+' tienda_name: '+str(self.tienda.name)+' ||| '+'entry_id:'+str(self.id)+' entry_name: '+str(self.title)

class Comment_entry(TimeStampedModel):
    """ Modelo para comentarios """
    entry = models.ForeignKey(
        Entry,
        verbose_name="entrada",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="usuario",
        related_name="user_entry_comment",
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey('self',related_name='children',on_delete=models.CASCADE, blank=True,null=True)
    parent_user = models.ForeignKey(
        User,
        verbose_name="usuario_response",
        on_delete=models.CASCADE,
        related_name="parent_user_entry_commnet",
        blank=True,
        null=True
    )
    text = models.CharField('comentario', max_length=255)
    
    class Meta:
        verbose_name = "Comentario entrada"
        verbose_name_plural = "Comentarios entradas"


    def __str__(self):
        return 'entrada_id: '+str(self.entry.id)+ ' entrada_name: '+str(self.entry.title)+ ' commnet_id: '+str(self.id) +' text: '+ self.text


class Images(TimeStampedModel):
    entry= models.ForeignKey(
        Entry,
        verbose_name='entrada',
        on_delete=models.CASCADE,
        related_name='images_entry',
    )
    image = models.ImageField(
        "Imagen", 
        upload_to="entry_images", 
        height_field=None, 
        width_field=None, 
        max_length=None,
        )
    tienda= models.ForeignKey(
        Tienda,
        verbose_name='tienda',
        on_delete=models.CASCADE,
        related_name='images_entry_tienda'
    )
 
    
    class Meta:
        verbose_name = "Imagen de la entrada"
        verbose_name_plural = "Imagenes de las entradas"

    def __str__(self):
        return 'entrada_id: '+str(self.entry.id)+ ' entrada_name: '+str(self.entry.title)+ ' image_id: '+str(self.id) +' image_url: '+ self.image.url

    
