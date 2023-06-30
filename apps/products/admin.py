from django.contrib import admin

from .models import (
    Category,
    Images,
    Product,
    Atributos,
    Atributos_Items,
    Variaciones,
    OpinionesProducts,
    PreguntaProduct
)

# Register your models here.


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Atributos_Items)
admin.site.register(Atributos)
admin.site.register(Variaciones)
admin.site.register(Images)
admin.site.register(OpinionesProducts)
admin.site.register(PreguntaProduct)
