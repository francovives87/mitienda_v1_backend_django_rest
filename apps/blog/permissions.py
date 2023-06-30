from rest_framework import permissions
from django.db.models import Count
from apps.tiendas.models import Tienda,Plan

from .models import Category_blog,Entry,Images



""" LOS IS_HE HAY QUE PONERLOS SIEMPRE QUE EN LOS REQUEST SE ENVIEN EL CAMPO TIENDA!!!,TANTO GET O POST """
""" este para los list, PARA LOS QUE ENVIAR LA TIENDA POR METODO GET """ 
class IsHe(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====request")
        print(request.user)
        print("request_META")
        print(request.query_params.get('tienda'))

        tienda_db = Tienda.objects.filter(
            user = request.user,
            id = request.query_params.get('tienda')
        )
        print("===tienda_DB")
        print(tienda_db)
        if (tienda_db):
            return True
        else:
            return False


""" ESTE ES PARA LOS RETRIEVE/UPDATE/DELETE, PARA LOS QUE ENVIAN LA TIENDA POR METODO POST """
class IsHe_2(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data['tienda'])

        tienda_db = Tienda.objects.filter(
            user = request.user,
            id = request.data['tienda']
        )
        if (tienda_db):
            return True
        else:
            return False

""" EL HAS OBJECT PERMISSION ES PARA LOS RETRIEVE """

class isOwner_category(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print (tienda.id)
        category = Category_blog.objects.get(id=obj.id)
        print("categody_db")
        print (category.tienda.id)
        if (category.tienda.id == tienda.id):
            return True
        else:
            return False

class isOwner_entry(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print (tienda.id)
        entry = Entry.objects.get(id=obj.id)
        print("categody_db")
        print (entry.tienda.id)
        if (entry.tienda.id == tienda.id):
            return True
        else:
            return False

class isOwner_image(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        #la tienda la saco del user, no hace falta enviarla por axios, muy inteligene!
        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print (tienda.id)
        images = Images.objects.get(id=obj.id)
        print("categody_db")
        print (images.tienda.id)
        if (images.tienda.id == tienda.id):
            return True
        else:
            return False

###### PERMISOS ESPECIALES PARA LA CREACION DE OBJETOS PARA MANEJO CON PLAN
###### BASADOS EN IS_HE2, MISMA FUNCION MAS AGREGADO DE CONTAR LA CANTIDAD DE PRODUCTOS
###### QUE HAY, Y QUE PUEDE CREER SEGUN SU PLAN.

class CanCreateCategorie(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data['tienda'])


        #uso value_list para limpiar el queryset, y traer el valor que necesito limpio
        tienda_db = Tienda.objects.filter(
            user = request.user,
            id = request.data['tienda']
        ).values_list('plan',flat=True)

        if (tienda_db):
            print(tienda_db)
            plan_id = tienda_db[0]
            print(plan_id)

            plan_db = Plan.objects.get(id=plan_id)
            
            print("cantidad de categorias permitidas")
            cant_categorie_allow = plan_db.blog_categories
            print(cant_categorie_allow)

            ###existe category

            existe_category_blog = Category_blog.objects.filter(
                tienda=request.data['tienda']
            )

            if existe_category_blog.exists():

                categories_blog = Category_blog.objects.filter(
                tienda=request.data['tienda']
                ).values('tienda').annotate(categories_blog=Count('tienda')).values_list('categories_blog',flat=True)
            
                print("Count de categorias creadas")
                cant_categories = categories_blog[0]
                print(cant_categories)
            else:
                cant_categories = 0


            if (cant_categories < cant_categorie_allow):
                return True
            else:
                return False
        else:
            return False


class CanCreateEntry(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data['tienda'])


        #uso value_list para limpiar el queryset, y traer el valor que necesito limpio
        tienda_db = Tienda.objects.filter(
            user = request.user,
            id = request.data['tienda']
        ).values_list('plan',flat=True)

        if (tienda_db):
            print(tienda_db)
            plan_id = tienda_db[0]
            print(plan_id)

            plan_db = Plan.objects.get(id=plan_id)
            
            print("cantidad de categorias permitidas")
            cant_entries_allow = plan_db.blog_entries
            print(cant_entries_allow)

            #existe registro
            existe_entry_reg = Entry.objects.filter(
                tienda=request.data['tienda']
            )

            if existe_entry_reg.exists():

                entries_blog = Entry.objects.filter(
                tienda=request.data['tienda']
                ).values('tienda').annotate(entries_blog=Count('tienda')).values_list('entries_blog',flat=True)
        
                print("Count de categorias creadas")
                cant_entries = entries_blog[0]
                print(cant_entries)
            else:
                cant_entries = 0

            if (cant_entries < cant_entries_allow):
                return True
            else:
                return False
        else:
            return False

class CanCreateMoreImages(permissions.BasePermission):

    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data['tienda'])


        #uso value_list para limpiar el queryset, y traer el valor que necesito limpio
        tienda_db = Tienda.objects.filter(
            user = request.user,
            id = request.data['tienda']
        ).values_list('plan',flat=True)

        if (tienda_db):
            print(tienda_db)
            plan_id = tienda_db[0]
            print(plan_id)

            plan_db = Plan.objects.get(id=plan_id)
            
            print("cantidad de categorias permitidas")
            cant_images_allow = plan_db.images_x_entries
            print(cant_images_allow)

            #primero veo si hay registros

            existe_registro = Images.objects.filter(
                entry=request.data['entry']
            )

            if existe_registro.exists(): 
            
                cant_images_db = Images.objects.filter(
                entry=request.data['entry']
                ).values('entry').annotate(cantidad=Count('id')).values_list('cantidad',flat=True)
                print("Count de categorias creadas")
                cant_images = cant_images_db[0]
                print(cant_images)
            else:
                cant_images_db = 0
                cant_images = 0

            print(cant_images_db)

            if (cant_images < cant_images_allow):
                return True
            else:
                return False
        else:
            return False






