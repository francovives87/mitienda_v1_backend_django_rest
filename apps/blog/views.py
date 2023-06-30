from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED,HTTP_400_BAD_REQUEST
from rest_framework import permissions
from django.db.models import Count,Avg, Max, Min

from rest_framework import serializers
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView,RetrieveAPIView  , UpdateAPIView
from .serializers import (
    EntrySerializerHome,
    CategoriesPrivate,
    EntryPrivateSerializer,
    CreateEntryPrivateSerializer,
    ImageSerializer,
    EntryDetailSerializer,
    EntryUpdatePublicSerializer,
    EntryUpdateContentSerializer,
    EntryPortadaImageSerializer,
    EntryPortadaSerializer,
    CategorySerializer,
    ListCommentsSerializer,
    PublicarComentarioParentSerializer,
    PublicarComentarioRespuestaSerializer
    )

from .models import Category_blog, Entry,Images,Comment_entry
# Create your views here.
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import (
    IsHe,
    IsHe_2,
    isOwner_category,
    isOwner_entry,
    isOwner_image,
    CanCreateCategorie,
    CanCreateEntry,
    CanCreateMoreImages
    )

class EntryList(ListAPIView):
    serializer_class = EntrySerializerHome

    def get_queryset(self):
        tienda = self.kwargs.get('pk',None)
        return Entry.objects.GetAllEntries(tienda)

class TiendaEntryDetailPublic(RetrieveAPIView):
    serializer_class = EntryDetailSerializer
    queryset = Entry.objects.all()

class GetAllEntriesForBlog(ListAPIView):
    serializer_class = EntrySerializerHome

    def get_queryset(self):
        tienda = self.request.query_params.get('tienda', '')
        return Entry.objects.filter(
            tienda=tienda,
            public=True,
        ).order_by("created")

class GetAllEntryCategories(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        tienda = self.request.query_params.get('tienda', '')
        return Category_blog.objects.filter(
            tienda=tienda
        )

class GetEntryByCategorie(ListAPIView):

    serializer_class = EntrySerializerHome

    def get_queryset(self):
        tienda = self.request.query_params.get('tienda', '')
        category = self.request.query_params.get('category', '')
        return Entry.objects.filter(
            tienda=tienda,
            category=category
        ).order_by("created")



############ PRIVATE ############################################################


############ CATEGORIAS #####################################################

class GetCategoriesOffTienda(ListAPIView):
    serializer_class = CategoriesPrivate
    permission_classes = [permissions.IsAuthenticated,IsHe]

    def get_queryset(self):
        tienda = self.request.query_params.get('tienda', '')
        return Category_blog.objects.filter(
            tienda=tienda,
            )

class GetEntrysOffCategory(ListAPIView):
    serializer_class = EntryPrivateSerializer
    permission_classes = [permissions.IsAuthenticated,IsHe]

    def get_queryset(self):
        tienda = self.request.query_params.get('tienda', '')
        category = self.request.query_params.get('category', '')
        return Entry.objects.filter(
            category=category,
            tienda=tienda,
            ).order_by("created")

class CreateCategoryBlogPrivate(CreateAPIView):
    serializer_class = CategoriesPrivate
    permission_classes = [permissions.IsAuthenticated,CanCreateCategorie]

class UpdateCategory(UpdateAPIView):
    serializer_class = CategoriesPrivate
    permission_classes = [permissions.IsAuthenticated,IsHe_2,isOwner_category]
    queryset= Category_blog.objects.all()

class DeleteCategoryPrivate(DestroyAPIView):
    serializer_class = CategoriesPrivate
    permission_classes = [permissions.IsAuthenticated,isOwner_category]
    queryset= Category_blog.objects.all()

################## ENTRADAS #####################################################


class CreateEntryPrivate(CreateAPIView):
    serializer_class = CreateEntryPrivateSerializer
    permission_classes = [permissions.IsAuthenticated,CanCreateEntry]

def modify_input_for_multiple_files(entry, image,tienda):
    dict = {}
    dict['entry'] = entry
    dict['image'] = image
    dict['tienda'] = tienda
    return dict


class CreateEntryImages(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated,IsHe_2]

    def get(self, request):
        all_images = Images.objects.all()
        serializer = ImageSerializer(all_images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        entry = request.data['entry']
        tienda = request.data['tienda']

        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(
                entry,
                img_name,
                tienda
                )
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

class CantImagesOffProduct(APIView):
    
    def get(self,request):
        entry = self.request.query_params.get('entry', '')
        cant_images = Images.objects.filter(
            entry=entry
        ).values('entry').annotate(cantidad=Count('id'))

                
        dict_res={
            "cant_images":0,
        }

        dict_res['cant_images'] = cant_images[0]['cantidad']

        return Response(dict_res,status=status.HTTP_200_OK)



class TiendaEntryDetail(RetrieveAPIView):
    serializer_class = EntryDetailSerializer
    queryset = Entry.objects.all()

class DeleteEntryPrivate(DestroyAPIView):
    serializer_class = EntryDetailSerializer
    permission_classes = [permissions.IsAuthenticated,isOwner_entry]
    queryset = Entry.objects.all()

class EntryPublicUpdate(UpdateAPIView):
    serializer_class = EntryUpdatePublicSerializer
    permission_classes = [permissions.IsAuthenticated,IsHe_2,isOwner_entry]
    queryset = Entry.objects.all()

class EntryPortadaUpdate(UpdateAPIView):
    serializer_class = EntryPortadaSerializer
    permission_classes = [permissions.IsAuthenticated,IsHe_2,isOwner_entry]
    queryset = Entry.objects.all()

class EntryUpdateContent(UpdateAPIView):
    serializer_class = EntryUpdateContentSerializer
    permission_classes = [permissions.IsAuthenticated,IsHe_2,isOwner_entry]
    queryset= Entry.objects.all()

class EditEntryPortadaImage(UpdateAPIView):
    serializer_class = EntryPortadaImageSerializer
    permission_classes = [permissions.IsAuthenticated,IsHe_2,isOwner_entry]
    queryset = Entry.objects.all()

class EditEntryImages(UpdateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated,IsHe_2,isOwner_image]
    queryset = Images.objects.all()

class DeleteEntryImages(DestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated,isOwner_image]
    queryset = Images.objects.all()

class ListComments(ListAPIView):
    serializer_class = ListCommentsSerializer

    def get_queryset(self):
        entry = self.request.query_params.get('entry', '')
        return Comment_entry.objects.filter(
            entry=entry,
            parent=None
        )

class CreateCommentParent(CreateAPIView):
    serializer_class = PublicarComentarioParentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CreateCommentResponse(CreateAPIView):
    serializer_class = PublicarComentarioRespuestaSerializer
    permission_classes = (permissions.IsAuthenticated,)

