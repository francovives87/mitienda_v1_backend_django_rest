from django.contrib import admin
from .models import (
    Service,
    Booking,
    AnonymousPersonalServiceData,
    Category_Service,
    Service_Images,
    OpinionesServices,
    PreguntaService,
    BookingMercadoPagoDetail
)

# Register your models here.
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(AnonymousPersonalServiceData)
admin.site.register(Category_Service)
admin.site.register(Service_Images)
admin.site.register(OpinionesServices)
admin.site.register(PreguntaService)
admin.site.register(BookingMercadoPagoDetail)
