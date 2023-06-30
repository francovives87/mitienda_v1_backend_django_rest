from django.urls import path, re_path

from . import views

app_name = 'orders_app'

urlpatterns = [ 
    path(
        'api/v1.0/orders/create',
        views.RegistrarOrden.as_view(),
        name='RegisterOrder'
    ),
    path(
        'api/v1.0/orders/anonymous/create',
        views.RegistrarOrdenAnonymous.as_view(),
        name='RegistrarOrdenAnonymous'
    ),
    path(
        'api/v1.0/orders/list/user/',
        views.OrderListForUser.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/tienda/orders/list/user/',
        views.OrderListForUserByTienda.as_view(),
        name='OrderListForUserByTienda'
    ),

    
    path(
        'api/v1.0/orders/detail/<pk>',
        views.OrderDetail.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/orders/anonymous/detail/<pk>',
        views.OrderDetailAnonymous.as_view(),
        name='ListOrderForUser'
    ),


    

    ###ADMIN
    path(
        'api/v1.0/admin/orders/<int:tienda>',
        views.GetOrdersOffTienda.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/news/',
        views.GetOrdersNewsOffTienda.as_view(),
        name='GetOrdersNewsOffTienda'
    ),
    path(
        'api/v1.0/admin/orders/news/count/',
        views.CountNewsOrders.as_view(),
        name='GetOrdersNewsOffTienda'
    ),    
    path(
        'api/v1.0/admin/orders/visto/',
        views.UpdateOrdenVisto.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/mercadopago',
        views.MercadoPagoInitPoint.as_view(),
        name='MercadoPagoInitPoint'
    ),
    path(
        'api/v1.0/anon/mercadopago',
        views.MercadoPagoInitPointAnonymous.as_view(),
        name='MercadoPagoInitPointAnonymous'
    ),

    path(
        'api/v1.0/admin/orders/mercadopago/status/<pk>',
        views.UpdateOrderMercadoPagoStatus.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/status/change/<pk>',
        views.OrderEstadoChange.as_view(),
        name='OrderEstadoChange'
    ),
    path(
        'api/v1.0/admin/orders/pay/change/<pk>',
        views.OrderPagoChange.as_view(),
        name='OrderPagoChange'
    ),
    path(
        'api/v1.0/admin/orders/delete/<pk>',
        views.DeleteOrder.as_view(),
        name='DeleteOrder'
    ),
    path(
        'api/v1.0/admin/orders/mercadopago/detail/create',
        views.CreateMercadoPagoOrderDetail.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/mercadopago/detail/',
        views.MercadoPagoDetail.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/search/date/',
        views.SearchOrderByDate.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/search/id/',
        views.SearchOrderById.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/filter/viewed/',
        views.FilterOrdersVistas.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/admin/orders/cancel/',
        views.CancelarOrden.as_view(),
        name='ListOrderForUser'
    ),
    path(
        'api/v1.0/anonymous/create/',
        views.CreateAnonymousData.as_view(),
        name='CreateAnonymousData'
    ),

    path(
        'api/v1.0/orders/novistas/clear/',
        views.ClearOrdersNoVistas.as_view(),
        name='ClearOrdersNoVistas'
    ),

    path(
        'api/v1.0/tienda/orders/permission/',
        views.CanCreateOrderByPlan.as_view(),
        name='CanCreateOrderByPlan'
    ),
    
]