from django.contrib import admin
from .models import (
    Tienda,
    Slider,
    Plan,
    Colors,
    Textures,
    Informacion,
    MercadoPago,
    Envios,
    Favoritos,
    Codigoqr,
    Geolocalization_geodjango,
    TiendaVisitor,
    Opiniones,
    Title_font,
    PaymentMethods,
    TransferData
)

# Register your models here.

admin.site.register(Tienda)
admin.site.register(Slider)
admin.site.register(Plan)
admin.site.register(Colors)
admin.site.register(Textures)
admin.site.register(Informacion)
admin.site.register(MercadoPago)
admin.site.register(Envios)
admin.site.register(Favoritos)
admin.site.register(Codigoqr)
admin.site.register(Geolocalization_geodjango)
admin.site.register(TiendaVisitor)
admin.site.register(Opiniones)
admin.site.register(Title_font)
admin.site.register(PaymentMethods)
admin.site.register(TransferData)

