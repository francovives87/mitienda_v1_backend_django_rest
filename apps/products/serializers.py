from rest_framework import serializers
from django.db.models import Count, Avg


from .models import (
    Atributos, 
    Product,
    Category,
    Atributos_Items,
    Variaciones,
    Images,
    OpinionesProducts,
    PreguntaProduct
)
from apps.products import models
from apps.users.models import User

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id','tienda','parent','name','image','children'
        )

class CategoryNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'name',
        )

class ListCategoriesSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField("get_children_field")

    
    def get_children_field(self, id):
            return Category.objects.filter(parent=id).values('id','name','image')
             
    class Meta:
        model = Category
        fields = ('id','tienda','parent','name','image','children')


class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            '__all__'
        )

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Images
        fields =('id','tienda','product','image')

class ProductPortadaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image',)

class UpdatePublicStatusProduct(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields =('tienda','public',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()
    images_product = ImageSerializer(many = True)

    class Meta:
        model = Product
        fields = (
            'id',
            'tienda',
            'category',
            'marca',
            'title',
            'description',
            'public',
            'image',
            'price',
            'portada',
            'in_offer',
            'in_offer_price',
            'has_variation',
            'has_options',
            'stock',
            'no_stock',
            'only_attribute',
            'images_product',
            'type',
            'visits'
        )

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()
    images_product = ImageSerializer(many = True)
    average= serializers.SerializerMethodField('get_average_field')
    count_opinion= serializers.SerializerMethodField('get_count_opinion_field')


    def get_average_field(self,id):
        return OpinionesProducts.objects.filter(
            product=id
        ).aggregate(Avg('rating'))

    def get_count_opinion_field(self,id):
        return OpinionesProducts.objects.filter(
            product=id
        ).aggregate(Count('opinion'))

    class Meta:
        model = Product
        fields = (
            'id',
            'tienda',
            'category',
            'marca',
            'title',
            'description',
            'public',
            'image',
            'price',
            'portada',
            'in_offer',
            'in_offer_price',
            'has_variation',
            'has_options',
            'stock',
            'no_stock',
            'only_attribute',
            'average',
            'images_product',
            'count_opinion',
            'type'
        )


class ProductToSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'category'
        )

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ('marca',)



#####################VARIACIONES##################################

class ArrayProductsSerializer(serializers.ListField):

    child = serializers.IntegerField()



class BuscarVariacionesSerializer(serializers.Serializer):

    product= serializers.IntegerField()
    item = ArrayProductsSerializer()


class Atributos_Items_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Atributos_Items
        fields = (
            'id',
            'item',
            )

class AtributosSerializer(serializers.ModelSerializer):

    atributo_item = Atributos_Items_Serializer(many=True)

    class Meta:
        model = Atributos
        fields = (
            'id',
            'nombre',
            'atributo_item',
            'repeat',
        )

class VariacionesSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    item = Atributos_Items_Serializer(many=True)

    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'stock',
            'price',
            'item',
            'no_stock',
        )


class CreateAtributoSerialiezer(serializers.ModelSerializer):
    
    class Meta:
        model = Atributos
        fields = ('__all__')

class CreateItemAtributoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Atributos_Items
        fields = ('__all__')


##########################CREATE VARIACION######################################3


class CreateAtributoItemVariacioneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atributos_Items
        fields = (
            'id',
            'atributo',
            'item',
        )

class CreateVariacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'item',
            'stock',
            'price',
            'no_stock'
        )

class UpdateVariacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variaciones
        fields = (
            'stock',
            'price',
        )


class GetVariationsOffProductSerializer(serializers.ModelSerializer):
    
    item = CreateAtributoItemVariacioneSerializer(many=True)

    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'item',
            'stock',
            'price',
            'no_stock'
        )

class ProductAndVariacionesForOrdersSerializer(serializers.ModelSerializer):

    item = Atributos_Items_Serializer(many=True)

    class Meta:
        model = Variaciones
        fields = (
            'id',
            'product',
            'stock',
            'price',
            'item',
            'no_stock'
        )

class StockVariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variaciones
        fields = ('no_stock','stock')


class PriceVariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variaciones
        fields = ('price',)

class HasVariationOnlyAttributeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('only_attribute','has_variation')


""" opiniones """

class OpinionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OpinionesProducts
        fields = (
            "product",
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
        model = OpinionesProducts
        fields = (
            "id",
            "user",
            "product",
            "rating",
            "opinion",
            "created"
            )

class UserOpinionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpinionesProducts
        fields = ("rating","opinion")

###PREGUNTAS


class PreguntaProductSerializer(serializers.ModelSerializer):

    user = UserOpinionSerializaer()

    class Meta:
        model = PreguntaProduct
        fields = (
            "id",
            "product",
            "user",
            "pregunta",
            "respuesta",
            "visto",
            "created",
            "modified"
            )


class ProductToPreguntaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "image",
        )

class PreguntaProductAdminSerializer(serializers.ModelSerializer):

    user = UserOpinionSerializaer()
    product = ProductToPreguntaSerializer()
    

    class Meta:
        model = PreguntaProduct
        fields = (
            "id",
            "product",
            "user",
            "pregunta",
            "respuesta",
            "visto",
            "created",
            "modified"
            )



class PreguntaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreguntaProduct
        fields = (
            "product",
            "pregunta",
            )

class PreguntaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreguntaProduct
        fields = (
            "respuesta",
            "visto"
        )

class ClearProductQuestionsNoVistasSerializer(serializers.Serializer):
    tienda = serializers.IntegerField()