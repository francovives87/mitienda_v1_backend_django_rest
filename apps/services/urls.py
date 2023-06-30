from django.urls import path, re_path

from . import views

app_name = "services_app"

urlpatterns = [
    ### ADMIN ###
    path(
        "api/v1.0/admin/bookings/count/",
        views.CountNewsOrders.as_view(),
        name="CountNewsOrders",
    ),
    path(
        "api/v1.0/admin/calendar/list/",
        views.GetApoimentsFromADate.as_view(),
        name="GetApoimentsFromADate",
    ),
    path(
        "api/v1.0/admin/calendar/all/",
        views.GetAllServicesAndApoimentsToCalendar.as_view(),
        name="GetAllServicesAndApoimentsToCalendar",
    ),
    path(
        "api/v1.0/admin/services/list/",
        views.ListServicesAdmin.as_view(),
        name="ListServicesAdmin",
    ),
    path(
        "api/v1.0/admin/services/create/",
        views.CreateService.as_view(),
        name="CreateService",
    ),
    path(
        "api/v1.0/admin/services/delete/<pk>",
        views.DeleteService.as_view(),
        name="DeleteService",
    ),
    path(
        "api/v1.0/admin/services/break/update/<pk>",
        views.ServiceBreakUpdate.as_view(),
        name="ServiceBreakUpdate",
    ),
    path(
        "api/v1.0/admin/bookings/news/",
        views.GetNewsBookingOffTienda.as_view(),
        name="GetNewsBookingOffTienda",
    ),
    path(
        "api/v1.0/admin/bookings/update/visto/<pk>",
        views.UpdateBookingVisto.as_view(),
        name="UpdateBookingVisto",
    ),
    path(
        "api/v1.0/user/booking/update/completed/<pk>",
        views.UpdateBookingCompleted.as_view(),
        name="UpdateBookingCompleted",
    ),
    path(
        "api/v1.0/admin/booking/<pk>",
        views.ViewBooking.as_view(),
        name="ViewBooking",
    ),
    path(
        "api/v1.0/user/booking/<pk>",
        views.UserViewBooking.as_view(),
        name="UserViewBooking",
    ),
    path(
        "api/v1.0/admin/booking/delete/<pk>",
        views.DeleteBooking.as_view(),
        name="DeleteBooking",
    ),
    path(
        "api/v1.0/admin/booking/novistas/delete/",
        views.ClearOrdersNoVistas.as_view(),
        name="ClearOrdersNoVistas",
    ),
    path(
        "api/v1.0/admin/services/categories/",
        views.GetCategoriesParentsPrivate.as_view(),
        name="GetCategoriesParentsPrivate",
    ),
    path(
        "api/v1.0/admin/services/categories/create/",
        views.CreateCategorie.as_view(),
        name="CreateCategorie",
    ),
    path(
        "api/v1.0/admin/services/subcategories/",
        views.GetSubCategoriesPrivate.as_view(),
        name="GetSubCategoriesPrivate",
    ),
    path(
        "api/v1.0/admin/services/categories/delete/<pk>/",
        views.DeleteCategoria.as_view(),
        name="DeleteCategoria",
    ),
    path(
        "api/v1.0/admin/services/categories/update/<pk>/",
        views.UpdateCategoria.as_view(),
        name="UpdateCategoria",
    ),
    path(
        "api/v1.0/admin/categories/services/",
        views.GetServicesOfCategoryPrivate.as_view(),
        name="GetServicesOfCategoryPrivate",
    ),
    path(
        "api/v1.0/admin/services/images/create/",
        views.CreateMoreServiceImages.as_view(),
        name="CreateMoreServiceImages",
    ),

    path(
        'api/v1.0/admin/service/delete/images/<pk>',
        views.DeleteServiceImages.as_view(),
        name='DeleteServiceImages'
    ),
   
    path(
        'api/v1.0/admin/service/image/<pk>',
        views.UpdatePortadaServiceImage.as_view(),
        name='UpdatePortadaServiceImage'
    ),
        path(
        'api/v1.0/admin/service/edit/images/<pk>',
        views.UpdateServicesImages.as_view(),
        name='UpdateServicesImages'
    ),

    
    path(
        "api/v1.0/admin/service/public/<pk>/",
        views.UpadatePublicStatusService.as_view(),
        name="UpadatePublicStatusService",
    ),
    path(
        "api/v1.0/admin/service/update/<pk>/",
        views.UpdateService.as_view(),
        name="UpdateService",
    ),

    path(
        'api/v1.0/admin/service/images/<int:service>',
        views.GetImagesOffService.as_view(),
        name='GetImagesOffService'
    ),
     path(
        'api/v1.0/admin/service/view/<pk>',
        views.ServiceDetailViewAdmin.as_view(),
        name='ServiceDetailViewAdmin'
    ),
    path(
        'api/v1.0/admin/service/images/count/',
        views.CantImagesOffService.as_view(),
        name='CantImagesOffService'
    ),
    path(
        'api/v1.0/admin/service/category/search/',
        views.SearchServicePrivateOnCategoryTriagram.as_view(),
        name='SearchServicePrivateOnCategoryTriagram'
    ),    

    ### FIN ADMIN ###
    ##TIENDA##
    path(
        "api/v1.0/services/categories/",
        views.GetCategoriesParents.as_view(),
        name="GetCategoriesParents",
    ),
    path(
        "api/v1.0/services/subcategories/",
        views.GetSubCategories.as_view(),
        name="GetSubCategories",
    ),
    path(
        "api/v1.0/service/category/detail/<pk>",
        views.CategoryDetailView.as_view(),
        name="CategoryDetailView",
    ),
    path(
        "api/v1.0/service/category/list/",
        views.GetServicesOfCategory.as_view(),
        name="GetServicesOfCategory",
    ),
    path("api/v1.0/services/list/", views.ServicesList.as_view(), name="ServicesList"),
    path(
        "api/v1.0/services/view/<pk>",
        views.ServiceDetailView.as_view(),
        name="ServiceDetailView",
    ),
    path(
        "api/v1.0/services/booking/create/",
        views.CreateBooking.as_view(),
        name="CreateBooking",
    ),
    path(
        "api/v1.0/services/booking/payment/create/",
        views.CreateBookingWithPayment.as_view(),
        name="CreateBookingWithPayment",
    ),

    #MercadoPago

    path(
        "api/v1.0/services/payment/mercadopago/",
        views.MercadoPagoInitPoint.as_view(),
        name="MercadoPagoInitPoint",
    ),
    path(
        "api/v1.0/services/payment/anon/mercadopago/",
        views.MercadoPagoInitPointAnonymous.as_view(),
        name="MercadoPagoInitPointAnonymous",
    ),
    path(
        'api/v1.0/admin/booking/mercadopago/detail/create',
        views.CreateMercadoPagoBookingDetail.as_view(),
        name='CreateMercadoPagoBookingDetail'
    ),


    


    

    
    path("api/v1.0/services/filter/", views.FilterDate.as_view(), name="FilterDate"),
    path(
        "api/v1.0/services/anonymous/create/",
        views.CreateAnonymousPersonalServiceData.as_view(),
        name="CreateAnonymousPersonalServiceData",
    ),
    path(
        "api/v1.0/user/bookings/",
        views.BookingsByUser.as_view(),
        name="BookingsByUser",
    ),
    path(
        "api/v1.0/tienda/user/bookings/",
        views.BookingsByUserByTienda.as_view(),
        name="BookingsByUserByTienda",
    ),
    path(
        "api/v1.0/tienda/bookings/permission/",
        views.CanCreateBooking.as_view(),
        name="CanCreateBooking",
    ),

    path(
        "api/v1.0/tienda/search/services/categories/",
        views.SearchOnTiendaServiceCategoryTriagram.as_view(),
        name="SearchOnTiendaServiceCategoryTriagram",
    ),
    path(
        "api/v1.0/tienda/search/services/",
        views.SearchServiceTiendaTriagram.as_view(),
        name="SearchServiceTiendaTriagram",
    ),
    path(
        "api/v1.0/tienda/search/services/categories/subcategories/",
        views.HasSubCategories.as_view(),
        name="HasSubCategories",
    ),
    path(
        "api/v1.0/tienda/search/services/on/categories/",
        views.SearchServiceOnCategoryTriagram.as_view(),
        name="SearchServiceOnCategoryTriagram",
    ),

    ########opiniones

    path(
        "api/v1.0/service/opinion/list/",
        views.GetOpinionesDeService.as_view(),
        name="GetOpinionesDeService",
    ),
        path(
        'api/v1.0/service/opinion/user/',
        views.GetUserOpinion.as_view(),
        name='GetUserOpinion'
    ),
    path(
        'api/v1.0/service/opinion/create/',
        views.CreateOpinion.as_view(),
        name='CreateOpinion'
    ),
    path(
        'api/v1.0/service/opinion/user/delete/<pk>',
        views.DeleteUserOpinion.as_view(),
        name='DeleteUserOpinion'
    ),
    path(
        'api/v1.0/service/opinion/user/update/<pk>',
        views.UpdateUserOpinion.as_view(),
        name='UpdateUserOpinion'
    ),


###Preguntas
    path(
        'api/v1.0/service/question/list/',
        views.PreguntasList.as_view(),
        name='PreguntasList'
    ),
    path(
        'api/v1.0/service/question/create/',
        views.PreguntaCreate.as_view(),
        name='PreguntaCreate'
    ),

    path(
        "api/v1.0/admin/service/questions/news/",
        views.GetNewsQuestionsOffTienda.as_view(),
        name="GetNewsQuestionsOffTienda",
    ),
    path(
        "api/v1.0/admin/service/questions/update/<pk>",
        views.UpdateQuestion.as_view(),
        name="UpdateQuestion",
    ),
    path(
        'api/v1.0/service/question/count/',
        views.CountNewsCuestions.as_view(),
        name='CountNewsCuestions'
    ),
    path(
        'api/v1.0/admin/service/question/novistas/',
        views.ClearServiceQuestionsNoVistas.as_view(),
        name='ClearServiceQuestionsNoVistas'
    ),
    path(
        'api/v1.0/admin/service/question/delete/<pk>',
        views.DeleteQuestion.as_view(),
        name='DeleteQuestion'
    ),


    


    


        
]
