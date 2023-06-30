from django import urls
from django.urls import path, re_path
from django.urls.conf import include

from . import views

app_name = 'tiendas_app'


urlpatterns = [
    path(
        'api/v1.0/tienda/<str:tienda>',
        views.GetTienda.as_view(),
        name='GetTienda'
    ),
    path(
        'api/v1.0/tienda/user/',
        views.GetTiendaByUserId.as_view(),
        name='GetTiendaByUserId'
    ),
    path(
        'api/v1.0/user/tienda/',
        views.UserHasTienda.as_view(),
        name='ListaProductsTienda'
    ),    
    path(
        'api/v1.0/tienda/slider/<pk>',
        views.GetSliderPublic.as_view(),
        name='ListaProductsTienda'
    ),
    path(
        'api/v1.0/tienda/colors/<int:tienda>',
        views.GetColorsOffTienda.as_view(),
        name='ListaProductsTienda'
    ),
    path(
        'api/v1.0/tienda/geo/exists/',
        views.ExisteGeolocation.as_view(),
        name='ExisteGeolocation'
    ),
    path(
        'api/v1.0/tienda/opinion/create/',
        views.CreateOpinion.as_view(),
        name='CreateOpinion'
    ),
    path(
        'api/v1.0/tienda/opinion/list/',
        views.GetOpinionesDeTinda.as_view(),
        name='GetOpinionesDeTinda'
    ),
    path(
        'api/v1.0/tienda/opinion/average/',
        views.PromedioTienda.as_view(),
        name='PromedioTienda'
    ),
    path(
        'api/v1.0/tienda/opinion/user/',
        views.GetUserOpinion.as_view(),
        name='GetUserOpinion'
    ),
    path(
        'api/v1.0/tienda/opinion/user/update/<pk>',
        views.UpdateUserOpinion.as_view(),
        name='UpdateUserOpinion'
    ),



    
    #####ADMIN

        path(
        'api/v1.0/admin/geo/update/<pk>',
        views.UpdateGeolocalization.as_view(),
        name='UpdateGeolocalization'
    ),


    path(
        'api/v1.0/admin/colors/update/<pk>/',
        views.UpdateColores.as_view(),
        name='AdminDeleteCategoria'
    ),
    path(
        'api/v1.0/admin/colors/update/texture/<pk>/',
        views.UpdateColoresWithTexture.as_view(),
        name='AdminDeleteCategoria'
    ),
    path(
        'api/v1.0/admin/textures/',
        views.ListTexures.as_view(),
        name='AdminDeleteCategoria'
    ),
    path(
        'api/v1.0/admin/tienda/information/update/<pk>/',
        views.UpdateTiendaInformation.as_view(),
        name='AdminDeleteCategoria'
    ),
    path(
        'api/v1.0/admin/tienda/logo/update/<pk>/',
        views.UpdateTiendaLogo.as_view(),
        name='AdminDeleteCategoria'
    ),
    path(
        'api/v1.0/admin/tienda/title/update/',
        views.UpdateTiendaTitle.as_view(),
        name='AdminDeleteCategoria'
    ),

    path(
        'api/v1.0/admin/tienda/slider/<pk>',
        views.GetSliderPrivate.as_view(),
        name='AdminGetSliderPrivate'
    ),
    path(
        'api/v1.0/admin/tienda/slider/update/<pk>/',
        views.UpdateSlider.as_view(),
        name='AdminUpdateSlider'
    ),
    path(
        'api/v1.0/admin/tienda/slider/delete/<pk>/',
        views.DeleteSlider.as_view(),
        name='AdminDeleteSlider'
    ),
    path(
        'api/v1.0/admin/tienda/slider/create/',
        views.CreateSlider.as_view(),
        name='AdminCreateSlider'
    ),
    path(
        'api/v1.0/admin/tienda/slider/public/<pk>/',
        views.SliderPublicUpdate.as_view(),
        name='AdminCreateSlider'
    ),
    path(
        'api/v1.0/tienda/create/',
        views.CreateTienda.as_view(),
        name='CreateTienda'
    ),

    path(
        'api/v1.0/admin/tienda/objects/',
        views.GetTotalObjectsCreatedOffTienda.as_view(),
        name='GetTotalObjectsCreatedOffTienda'
    ),
    path(
        'api/v1.0/admin/tienda/mercadopago/credentials/',
        views.MercadoPagoCredentialsExists.as_view(),
        name='MercadoPagoCredentialsExists'
    ),
    path(
        'api/v1.0/admin/tienda/mercadopago/credentials/create/',
        views.MercadoPagoCredentialsCreateOrUpdate.as_view(),
        name='MercadoPagoCredentialsCreateOrUpdate'
    ),
        path(
        'api/v1.0/admin/tienda/transfer/credentials/',
        views.TransferCredentialsExists.as_view(),
        name='TransferCredentialsExists'
    ),
    path(
        'api/v1.0/admin/tienda/transfer/credentials/create/',
        views.TransferDataCredentialsCreateOrUpdate.as_view(),
        name='TransferDataCredentialsCreateOrUpdate'
    ),
    
    path(
        'api/v1.0/admin/envio/create/',
        views.CreateEnvio.as_view(),
        name='CreateEnvio'
    ),
    path(
        'api/v1.0/admin/envio/',
        views.ListEnvios.as_view(),
        name='ListEnvios'
    ),
    path(
        'api/v1.0/admin/envio/update/<pk>',
        views.UpdateEnvio.as_view(),
        name='ListEnvios'
    ),
    path(
        'api/v1.0/admin/envio/delete/<pk>',
        views.DeleteEnvio.as_view(),
        name='ListEnvios'
    ),
    path(
        'api/v1.0/store/search/',
        views.SearchTiendaTriagram.as_view(),
        name='ListEnvios'
    ),
    path(
        'api/v1.0/store/search/description/',
        views.SearchTiendaByDescription.as_view(),
        name='SearchTiendaByDescription'
    ),
    path(
        'api/v1.0/admin/store/type/<pk>',
        views.TipoDeTienda.as_view(),
        name='ListEnvios'
    ),
    path(
        'api/v1.0/store/favorites/',
        views.ListFavoritos.as_view(),
        name='ListFavoritos'
    ),
    path(
        'api/v1.0/store/favorites/create/',
        views.CreateFavorite.as_view(),
        name='CreateFavorite'
    ),
    path(
        'api/v1.0/store/favorites/exists/',
        views.UserHasThisFavorite.as_view(),
        name='UserHasThisFavorite'
    ),
    path(
        'api/v1.0/store/favorites/delete/<pk>',
        views.DeleteFavorite.as_view(),
        name='DeleteFavorite'
    ),
    path(
        'api/v1.0/store/qrcode/create/',
        views.CreateQrCode.as_view(),
        name='CreateQrCode'
    ),
    path(
        'api/v1.0/store/qrcode/get/',
        views.GetQrCode.as_view(),
        name='GetQrCode'
    ),  
    path(
        'api/v1.0/admin/geo/create/',
        views.CreateGeoDjango.as_view(),
        name='CreateGeoDjango'
    ),

    path(
        'api/v1.0/store/geo/news/',
        views.GeoDjangoNewsStoresNears.as_view(),
        name='GeoDjangoNewsStoresNears'
    ),
    path(
        'api/v1.0/store/search/filter/',
        views.SearchFilterByLocation.as_view(),
        name='SearchFilterByLocation'
    ),
    path(
        'api/v1.0/store/search/filter/cities/by/subregion/',
        views.FilterCitiesBySubregion.as_view(),
        name='FilterCitiesBySubregion'
    ),
    path(
        'api/v1.0/store/search/filter/cities/by/region/',
        views.FilterDepartamentosByRegion.as_view(),
        name='FilterDepartamentosByRegion'
    ),
    path(
        'api/v1.0/store/search/global/store/',
        views.SearchGlobalStoreByTitle.as_view(),
        name='SearchGlobalStoreByTitle'
    ),
    path(
        'api/v1.0/store/search/global/store/keyword/',
        views.SearchGlobalStoreByDescription.as_view(),
        name='SearchGlobalStoreByDescription'
    ),
    path(
        'api/v1.0/store/destacadas/',
        views.GetTiendasDestacadas.as_view(),
        name='GetTiendasDestacadas'
    ),

    path(
        'api/v1.0/store/demos/',
        views.GetTiendasDemo.as_view(),
        name='GetTiendasDemo'
    ),


    
    path(
        'api/v1.0/store/title/fonts/',
        views.TiendaTitleFont.as_view(),
        name='TiendaTitleFont'
    ),
    path(
        'api/v1.0/fonts/title/',
        views.GetTitleFonts.as_view(),
        name='GetTitleFonts'
    ),

    path(
        'api/v1.0/store/title/font/update/<pk>',
        views.UpdateTitleFont.as_view(),
        name='UpdateTitleFont'
    ),
    path(
        'api/v1.0/store/visitor/create/',
        views.CreateTiendaVisitor.as_view(),
        name='CreateTiendaVisitor'
    ),
    path(
        'api/v1.0/store/visitor/all/',
        views.GetTiendaVisitor.as_view(),
        name='GetTiendaVisitor'
    ),
    path(
        'api/v1.0/admin/tienda/paymentmethods/update/',
        views.UpdatePaymentsMethods.as_view(),
        name='UpdatePaymentsMethods' 
    ),

     
]