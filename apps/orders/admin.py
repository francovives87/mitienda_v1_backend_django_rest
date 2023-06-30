from django.contrib import admin

from .models import (Order,Order_detail,OrderMercadoPagoDetail,AnonymousPersonalData,Ticket)
# Register your models here.


admin.site.register(Order)
admin.site.register(Order_detail)
admin.site.register(OrderMercadoPagoDetail)
admin.site.register(AnonymousPersonalData)
admin.site.register(Ticket)

