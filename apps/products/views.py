from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework import permissions
from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count, Avg, Max, Min
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from apps import tiendas

from apps.products.models import (
    Atributos_Items,
    Category,
    Product,
    Variaciones,
    Atributos,
    Images,
    OpinionesProducts,
    PreguntaProduct
)
from apps.blog.models import Category_blog, Entry
from apps.tiendas import serializers
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    CreateProductSerializer,
    BuscarVariacionesSerializer,
    AtributosSerializer,
    VariacionesSerializer,
    CreateItemAtributoSerializer,
    CreateAtributoSerialiezer,
    CreateVariacionesSerializer,
    GetVariationsOffProductSerializer,
    ImageSerializer,
    UpdatePublicStatusProduct,
    ProductPortadaImageSerializer,
    ProductAndVariacionesForOrdersSerializer,
    Atributos_Items_Serializer,
    HasVariationOnlyAttributeSerializer,
    UpdateVariacionesSerializer,
    ProductToSearchSerializer,
    OpinionCreateSerializer,
    OpinionListSerializer,
    UserOpinionUpdateSerializer,
    PreguntaProductSerializer,
    PreguntaCreateSerializer,
    PreguntaProductAdminSerializer,
    PreguntaUpdateSerializer,
    ClearProductQuestionsNoVistasSerializer,
    ListCategoriesSerializer,
    MarcaSerializer
)

# Permisos

from .permissions import (
    IsHe,
    IsHe_2,
    isOwner_category,
    isOwner_product,
    isOwner_image,
    isOwner_atributo,
    isOwner_variacion,
    CanCreateCategorie,
    CanCreateProduct,
    CanCreateMoreImages,
)

# Create your views here.

##################################PRODUTOS_TIENDA############################################

######Vistas publicas############
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        return Product.objects.all()


class ListProductsInTienda(ListAPIView):
    serializer_class = ProductSerializer
    """ permission_classes = (permissions.IsAuthenticated,) """

    def get_queryset(self):
        return Product.objects.all()


class ListSalientProducts(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("tienda", None)
        return Product.objects.producto_destacado(tienda)


class ListProductsOff(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("tienda", None)
        return Product.objects.producto_en_ofertas(tienda)


class ListProductsNews(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        tienda = self.kwargs.get("tienda", None)
        return Product.objects.producto_nuevos(tienda)


class SearchProduct(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")
        return Product.objects.search_product_trg(kword, tienda)


class SearchProductIcontains(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")
        return Product.objects.search_product_icontais(kword, tienda)


###CATEGORIAS####


class ListCategoriesParent(ListAPIView):
    serializer_class = ListCategoriesSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Category.objects.filter(
            tienda=tienda,
            parent =None
        )


class ListSubCategories(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        return Category.objects.filter(parent__id=kword)

class ListCategories(ListAPIView):
    serializer_class = ListCategoriesSerializer
    
    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", None)
        return Category.objects.filter(tienda=tienda)

class GetSubCategory(ListAPIView):
    serializer_class = CategorySerializer



###FILTROS PRODUCTOS###


class FilterProductCheap(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        Kwordctg = self.request.query_params.get("Kwordctg", "")
        return Product.objects.Filer_product_cheap(Kwordctg)


class FilterProductInOffert(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        Kwordctg = self.request.query_params.get("Kwordctg", "")
        return Product.objects.Filer_product_on_offert(Kwordctg)

class MarcasOnCategories(ListAPIView):
    serializer_class = MarcaSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category", None)
        return Product.objects.all().filter(
            category= category
        ).distinct("marca")

class FilterByMarca(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        marca = self.request.query_params.get("marca", None)
        category = self.request.query_params.get("category", None)
        return Product.objects.filter(
            marca = marca,
            category = category
        )

##################################PRODUTOS_TIENDA############################################


###CATEGORIAS####


####################CATEGORIAS_TIENDA#######################

##con foreingkey relased_name="children" en el modelo, obtento la relacion inversa
## es decir, yo pongo el id de un subcategoria, y me dice quien es el padre
class ListSubCategoriesInverse(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        return Category.objects.filter(children__id=kword)


class CategoryDetailView(RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class GetProductsOfCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        return Product.objects.GetProductsOfCategory(kword)


class SearchProductOnCategory(ListAPIView):
    serializer_class = ProductToSearchSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        category = self.request.query_params.get("category", "")
        tienda = self.request.query_params.get("tienda", "")

        return Product.objects.filter(
            title__trigram_similar=kword,
            category=category,
            tienda=tienda,
            public=True,
        )


class HasSubCategories(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category = self.request.query_params.get("category", "")
        tienda = self.request.query_params.get("tienda", "")

        return Category.objects.filter(parent=category, tienda=tienda)


class SearchProductOnCategoryIcontains(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        Kwordctg = self.request.query_params.get("Kwordctg", "")
        return Product.objects.search_product_IcontainsOnCategory(kword, Kwordctg)


class SearchCategoryWithTgr(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")
        return Category.objects.search_category_trg(kword, tienda)


####################CATEGORIAS_TIENDA#######################

########CATEGORIAS ADMIN#######

##############VISTAS PRIVADAS!! ###################


class GetCateogiesPrivate(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsHe]

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return Category.objects.categories_parent(tienda)


class AddPrincipalCategoria(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateCategorie]


class DeleteCategoria(DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_category]
    queryset = Category.objects.all()


class UpdateCategoria(UpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_category]
    queryset = Category.objects.all()


class GetTotalObjectsCreatedOffTienda(APIView):
    def get(self, request):
        tienda = self.request.query_params.get("tienda", "")
        categories = (
            Category.objects.filter(tienda=tienda)
            .values("tienda")
            .annotate(categorias=Count("tienda"))
        )

        productos = (
            Product.objects.filter(tienda=tienda)
            .values("tienda")
            .annotate(productos=Count("tienda"))
        )

        categories_blog = (
            Category_blog.objects.filter(tienda=tienda)
            .values("tienda")
            .annotate(categories_blog=Count("tienda"))
        )

        entries_blog = (
            Entry.objects.filter(tienda=tienda)
            .values("tienda")
            .annotate(entries_blog=Count("tienda"))
        )

        res_array = []
        res_array.append(categories)
        res_array.append(productos)
        res_array.append(categories_blog)
        res_array.append(entries_blog)

        return Response(res_array, status=status.HTTP_201_CREATED)


#######CATEGORIAS ADMIN#######


#######PRODUCTOS ADMIN#######


class GetProductsOfCategoryPrivate(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsHe]

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")

        return Product.objects.GetProductsOfCategoryPrivate(kword, tienda)


class ProductDetailViewAdmin(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class CreateProduct(CreateAPIView):
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateProduct]


class DeleteProduct(DestroyAPIView):
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_product]
    queryset = Product.objects.all()


class UpdateProduct(UpdateAPIView):
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_product]
    queryset = Product.objects.all()


class UpadatePublicStatusProduct(UpdateAPIView):
    serializer_class = UpdatePublicStatusProduct
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_product]
    queryset = Product.objects.all()


class SearchProductOnCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")
        category = self.request.query_params.get("category", "")
        return Product.objects.search_product_on_category_trg(kword, tienda, category)


class SearchProductIcontainsOnCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        tienda = self.request.query_params.get("tienda", "")
        category = self.request.query_params.get("category", "")
        return Product.objects.search_product_icontais_on_category(
            kword, tienda, category
        )


# Multiple image uploads
def modify_input_for_multiple_files(product, image, tienda):
    dict = {}
    dict["product"] = product
    dict["image"] = image
    dict["tienda"] = tienda
    return dict


class CreateMoreProductImages(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated,
        CanCreateMoreImages,
        isOwner_product,
    ]

    def get(self, request):
        all_images = Images.objects.all()
        serializer = ImageSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        product = request.data["product"]
        tienda = request.data["tienda"]

        # converts querydict to original dict
        images = dict((request.data).lists())["image"]
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(product, img_name, tienda)
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


class GetImagesOffProduct(ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        product = self.kwargs.get("product", None)
        return Images.objects.filter(product=product)


class CantImagesOffProduct(APIView):
    def get(self, request):
        product = self.request.query_params.get("product", "")
        cant_images = (
            Images.objects.filter(product=product)
            .values("product")
            .annotate(cantidad=Count("id"))
        )

        dict_res = {
            "cant_images": 0,
        }

        dict_res["cant_images"] = cant_images[0]["cantidad"]

        return Response(dict_res, status=status.HTTP_200_OK)


class EditProductPortadaImage(UpdateAPIView):
    serializer_class = ProductPortadaImageSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_product]
    queryset = Product.objects.all()


class EditProductImages(UpdateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsHe_2, isOwner_image]
    queryset = Images.objects.all()


class DeleteProductImages(DestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_image]
    queryset = Images.objects.all()


#######PRODUCTOS ADMIN#######


#########################Variaciones#########################################


class BuscarVariaciones(GenericAPIView):
    allowed_methods = ["POST"]
    serializer_class = BuscarVariacionesSerializer

    def post(self, request):
        serializer = BuscarVariacionesSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        respuesta = (
            Variaciones.objects.all()
            .filter(
                product=serializer.validated_data["product"],
                item__in=serializer.validated_data["item"],
            )
            .values("pk")
            .annotate(repeticiones=Count("pk"))
        )

        serialized_q = json.dumps(list(respuesta), cls=DjangoJSONEncoder)

        return HttpResponse(serialized_q, content_type="application/json")


class ListAtributosWithItemsforProduct(ListAPIView):

    serializer_class = AtributosSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        return Atributos.objects.AtributosWithItemForProduct(kword)


class ListVariacionEncontrdas(RetrieveAPIView):

    serializer_class = VariacionesSerializer

    def get_queryset(self):
        return Variaciones.objects.all()


class GetProductAndVariacionForOrderDetail(ListAPIView):
    serializer_class = ProductAndVariacionesForOrdersSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product", "")
        variation = self.request.query_params.get("variation", "")

        return Variaciones.objects.filter(product=product, id=variation)


#########creacion/eliminacion/edicion atributos#################


class CreateAtributo(CreateAPIView):
    serializer_class = CreateAtributoSerialiezer
    permission_classes = [permissions.IsAuthenticated, isOwner_product]


class DeleteAtributoDelProducto(DestroyAPIView):
    serializer_class = AtributosSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_atributo]
    queryset = Atributos.objects.all()


class CreateItemAtributo(CreateAPIView):
    serializer_class = CreateItemAtributoSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_atributo]


class GetItem(ListAPIView):
    serializer_class = Atributos_Items_Serializer

    def get_queryset(self):
        item = self.kwargs.get("item", None)
        return Atributos_Items.objects.filter(id=item)


##########################CREAR/EDITAR/ELIMINAR VARIACIONES####################################3


class GetVariationsOffProduct(ListAPIView):
    serializer_class = GetVariationsOffProductSerializer

    def get_queryset(self):
        kword = self.request.query_params.get("kword", "")
        return Variaciones.objects.filter(product=kword)


class VariacionViewSet(viewsets.ModelViewSet):
    serializer_class = CreateVariacionesSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_product]
    """ solo permito estos verbos http, porque el delete lo hago aparte por el tema de los permisos """
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):

        variaciones = Variaciones.objects.all()
        return variaciones


class DeleteVariacion(DestroyAPIView):
    serializer_class = CreateVariacionesSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_variacion]
    queryset = Variaciones.objects.all()


class UpdateVariacion(UpdateAPIView):
    serializer_class = UpdateVariacionesSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner_variacion]
    queryset = Variaciones.objects.all()


""" Obtener minimo precio de variacion, para mostrar precio desde """


class MinPriceVariacion(ListAPIView):
    serializer_class = CreateVariacionesSerializer

    def get_queryset(self):
        product = self.kwargs.get("product", None)
        return (
            Variaciones.objects.all()
            .filter(
                product=product,
            )
            .order_by("price")[0:1]
        )


class HasVariationOnlyAttributeUpdate(UpdateAPIView):
    serializer_class = HasVariationOnlyAttributeSerializer
    queryset = Product.objects.all()


""" opiniones """


class CreateOpinion(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        serializer = OpinionCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        product_request = serializer.validated_data["product"]

        print(user)

        existe_opinion = OpinionesProducts.objects.filter(
            user=user, product=product_request
        )

        if existe_opinion.exists():

            return Response({"msj": "Ya ha comentado"}, status=HTTP_200_OK)

        else:
            OpinionesProducts.objects.create(
                product=product_request,
                user=user,
                rating=serializer.validated_data["rating"],
                opinion=serializer.validated_data["opinion"],
            )

            return Response({"msj": "Comentario Creado!"}, status=HTTP_200_OK)


class GetOpinionesDeProduct(ListAPIView):
    serializer_class = OpinionListSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product")

        return OpinionesProducts.objects.filter(product=product).order_by("created")


class GetUserOpinion(ListAPIView):
    serializer_class = OpinionListSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product")
        user = self.request.query_params.get("user")
        return OpinionesProducts.objects.filter(product=product, user=user)[0:1]


class DeleteUserOpinion(DestroyAPIView):
    serializer_class = OpinionListSerializer
    queryset = OpinionesProducts.objects.all()

class UpdateUserOpinion(UpdateAPIView):
    serializer_class = UserOpinionUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = OpinionesProducts.objects.all()


##Preguntas

class PreguntasList(ListAPIView):
    serializer_class = PreguntaProductSerializer

    def get_queryset(self):
        product = self.request.query_params.get("product", None)
        return PreguntaProduct.objects.filter(
            product=product
        ).order_by("-created")


class PreguntaCreate(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        serializer = PreguntaCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        product_request = serializer.validated_data["product"]

    
        createQuestion = PreguntaProduct.objects.create(
            user = user,
            product=product_request,
            pregunta=serializer.validated_data["pregunta"],
        )

        print("createQuestion")
        print(createQuestion.product.tienda.id)
        tienda_id = createQuestion.product.tienda.id

        """ Envio la noticifacion a channel """

        res = {"tienda_id": tienda_id}
        print(res)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifi", {"type": "send_notifi_question", "text": json.dumps(res)}
        )
 
        return Response({"msj": "Pregunta Creada!"}, status=HTTP_200_OK)


class CountNewsCuestions(APIView):
    def get(self, request):
        tienda = self.request.query_params.get("tienda", "")
        dict_res = {
            "preguntas_nuevas": 0,
        }

        existe_ordenes = PreguntaProduct.objects.filter(
            product__tienda=tienda, 
            visto=False
            )

        if existe_ordenes.exists():

            preguntas_news = (
                PreguntaProduct.objects.filter(product__tienda=tienda, visto=False)
                .values("product__tienda")
                .annotate(preguntas=Count("product__tienda"))
            )
            dict_res["preguntas_nuevas"] = preguntas_news[0]["preguntas"]

        return Response(dict_res, status=status.HTTP_200_OK)


class GetNewsQuestionsOffTienda(ListAPIView):
    serializer_class = PreguntaProductAdminSerializer

    def get_queryset(self):
        tienda = self.request.query_params.get("tienda", "")
        return PreguntaProduct.objects.filter(
            product__tienda=tienda, 
            visto=False
            ).order_by("-created")

class UpdateQuestion(UpdateAPIView):
    serializer_class = PreguntaUpdateSerializer
    queryset = PreguntaProduct.objects.all()


class DeleteQuestion(DestroyAPIView):
    serializer_class = PreguntaProductAdminSerializer
    queryset = PreguntaProduct.objects.all()



class ClearProductQuestionsNoVistas(APIView):

    serializer_class = ClearProductQuestionsNoVistasSerializer

    def post(self, request, *args, **kwargs):

        serializer = ClearProductQuestionsNoVistasSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        tienda = serializer.validated_data["tienda"]

        bookings_db = PreguntaProduct.objects.filter(
            product__tienda=tienda, visto=False
        ).update(visto=True)

        print(bookings_db)

        return Response({"msj": "OK"}, status=HTTP_200_OK)