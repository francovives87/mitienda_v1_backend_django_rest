from django.db.models.expressions import F
from rest_framework import permissions
from apps.tiendas.models import Tienda, Plan
from .models import Service,Category_Service,Service_Images
from django.db.models import Count


class IsHe(permissions.BasePermission):
    def has_permission(self, request, view):
        print("====request")
        print(request.user)
        print("request_META")
        print(request.query_params.get("tienda"))

        tienda_db = Tienda.objects.filter(
            user=request.user, id=request.query_params.get("tienda")
        )
        print("===tienda_DB")
        print(tienda_db)
        if tienda_db:
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


class isOwner_service(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print (tienda.id)
        service = Service.objects.get(id=obj.id)
        print("categody_db")
        print (service.tienda.id)
        if (service.tienda.id == tienda.id):
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
        images = Service_Images.objects.get(id=obj.id)
        print("categody_db")
        print (images.tienda.id)
        if (images.tienda.id == tienda.id):
            return True
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
            cant_images_allow = plan_db.images_x_services
            print(cant_images_allow)

            #primero veo si hay registros

            existe_registro = Service_Images.objects.filter(
                service=request.data['service']
            )

            if existe_registro.exists(): 
            
                cant_images_db = Service_Images.objects.filter(
                service=request.data['service']
                ).values('service').annotate(cantidad=Count('id')).values_list('cantidad',flat=True)
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

        

class isOwner_category(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        print('ACa que onda?')
        print("queryset")

        tienda = Tienda.objects.get(user=request.user)
        print("user_tienda")
        print (tienda.id)
        category = Category_Service.objects.get(id=obj.id)
        print("categody_db")
        print (category.tienda.id)
        if (category.tienda.id == tienda.id):
            return True
        else:
            return False

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
            cant_categorie_allow = plan_db.services_categories
            print(cant_categorie_allow)

            ##existe category

            existe_categoria = Category_Service.objects.filter(
                tienda=request.data['tienda']
            )

            if existe_categoria.exists():

                categories = Category_Service.objects.filter(
                tienda=request.data['tienda']
                ).values('tienda').annotate(categorias=Count('tienda')).values_list('categorias',flat=True)
        
                print("Count de categorias creadas")
                cant_categories = categories[0]
                print(cant_categories)
            else:
                cant_categories = 0

            if (cant_categories < cant_categorie_allow):
                return True
            else:
                return False
        else:
            return False


class CanCreateService(permissions.BasePermission):
    def has_permission(self, request, view):
        print("====IsHE_2")
        print(request.data["tienda"])

        # uso value_list para limpiar el queryset, y traer el valor que necesito limpio
        tienda_db = Tienda.objects.filter(
            user=request.user, id=request.data["tienda"]
        ).values_list("plan", flat=True)

        if tienda_db:
            print(tienda_db)
            plan_id = tienda_db[0]
            print(plan_id)

            plan_db = Plan.objects.get(id=plan_id)

            print("cantidad de services permitidos")
            cant_service_allow = plan_db.services
            print(cant_service_allow)

            ### existe product?

            existe_products = Service.objects.filter(tienda=request.data["tienda"])

            if existe_products.exists():

                productos = (
                    Service.objects.filter(tienda=request.data["tienda"])
                    .values("tienda")
                    .annotate(services=Count("tienda"))
                    .values_list("services", flat=True)
                )

                print("Count de categorias creadas")
                cant_services = productos[0]
                print(cant_services)
            else:
                cant_services = 0

            if cant_services < cant_service_allow:
                return True
            else:
                return False
        else:
            return False
