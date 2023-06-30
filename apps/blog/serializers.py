from attr import fields
from rest_framework import serializers
from django.db.models import F, Func, Value, CharField
from .models import Entry, Images, Tag, Category_blog, Comment_entry
from apps.users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_blog
        fields = (
            "name",
            "id",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class EntrySerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Entry
        fields = "__all__"


class EntrySerializerHome(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Entry
        fields = ("id", "title", "content", "image", "category")


class CategoriesPrivate(serializers.ModelSerializer):
    class Meta:
        model = Category_blog
        fields = "__all__"


class EntryPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"


class CreateEntryPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ("id", "tienda", "entry", "image")


class EntryDetailSerializer(serializers.ModelSerializer):

    images_entry = ImageSerializer(many=True)

    class Meta:
        model = Entry
        fields = (
            "id",
            "title",
            "category",
            "content",
            "image",
            "images_entry",
        )


class EntryUpdatePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ("public", "tienda")


class EntryPortadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ("portada", "tienda")


class EntryUpdateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ("title", "content", "tienda")


class EntryPortadaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ("image", "tienda")


#####COMMENTS


class UserNameCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username")


class ListCommentsSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField("get_response_field")
    user = UserNameCommentSerializer()

    def get_response_field(self, id):
        return (
            Comment_entry.objects.filter(parent=id)
            .values(
                "id",
                "user__username",
                "user__id",
                "text",
                "parent",
                "parent_user__username",

            ) 
            ##funcion annotate para formatear la fecha!!
            ##hay que importar ("from django.db.models import F, Func, Value, CharField")
            ##estas librerias
            .annotate(
                formatted_date=Func(
                    F("created"),
                    Value("DD-MM-YYYY HH:MM:SS"),
                    function="to_char",
                    output_field=CharField(),
                )
            )
        )

    class Meta:
        model = Comment_entry
        fields = ("id", "created", "user", "entry", "parent", "text", "response")


class PublicarComentarioParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment_entry
        fields= ("entry","text","user")

class PublicarComentarioRespuestaSerializer(serializers.ModelSerializer):

    class Meta:
        model= Comment_entry
        fields = ("__all__")