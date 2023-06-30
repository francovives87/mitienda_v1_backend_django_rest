from django.urls import path, re_path

from . import views

app_name = 'estadisticas_app'

urlpatterns = [
    path(
        'api/v1.0/tienda/statics/list/order/cant/products/',
        views.ListCantProductsOnOrder.as_view(),
        name='ListCantProductsOnOrder'
    ),
    path(
        'api/v1.0/tienda/statics/list/order/have/products/',
        views.ListOrdersWhereHaveProduct.as_view(),
        name='ListOrdersWhereHaveProduct'
    ),    
]