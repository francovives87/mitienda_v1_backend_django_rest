from django.db.models.expressions import F
from rest_framework import permissions
from .models import Tienda,Plan,Slider
from django.db.models import Count

class CanCreateSlide(permissions.BasePermission):

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
            
            print("cantidad de sliders permitidos")
            cant_slide_allow = plan_db.images_sliders
            print(cant_slide_allow)

            ### existe Slider?

            existe_slider = Slider.objects.filter(
                tienda=request.data['tienda']
            )

            if existe_slider.exists():

                slider = Slider.objects.filter(
                tienda=request.data['tienda']
                ).values('tienda').annotate(slide=Count('tienda')).values_list('slide',flat=True)
            
                print("Count de categorias creadas")
                cant_slide = slider[0]
                print(cant_slide)
            else:
                cant_slide = 0


            if (cant_slide < cant_slide_allow):
                return True
            else:
                return False
        else:
            return False
