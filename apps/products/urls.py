from django import urls
from django.urls import path, re_path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter


from . import views

app_name = 'products_app'


router = DefaultRouter()
router.register('variaciones',views.VariacionViewSet,basename="variaciones")



urlpatterns = [
    path(
        'api/v1.0/products/list',
        views.ListProductsInTienda.as_view(),
        name='ListaProductsTienda'
    ),
    path(
        'api/v1.0/products/salients/list/<tienda>',
        views.ListSalientProducts.as_view(),
        name='ListProductsSalints'
    ),
    path(
        'api/v1.0/products/off/list/<tienda>',
        views.ListProductsOff.as_view(),
        name='ListProductsOff'
    ),
    path(
        'api/v1.0/products/detail/<pk>',
        views.ProductDetailView.as_view(),
        name='ListProductsDetail'
    ),
    path(
        'api/v1.0/products/news/<int:tienda>',
        views.ListProductsNews.as_view(),
        name='ListProductsNews'
    ),
    path(
        'api/v1.0/products/search/',
        views.SearchProduct.as_view(),
        name='ProductsSearch'
    ),
    path(
        'api/v1.0/products/search/icontains/',
        views.SearchProductIcontains.as_view(),
        name='ProductsSearchIcontains'
    ),
    path(
        'api/v1.0/admin/product/search/icontains/',
        views.SearchProductIcontainsOnCategory.as_view(),
        name='ProductsSearchIcontainsOnCategory'
    ),

    path(
        'api/v1.0/categories/product/cheap/',
        views.FilterProductCheap.as_view(),
        name='ProductsSearch'
    ),
    path(
        'api/v1.0/categories/product/inoffert/',
        views.FilterProductInOffert.as_view(),
        name='ProductsSearch'
    ),
    path(
        'api/v1.0/product/opinion/create/',
        views.CreateOpinion.as_view(),
        name='CreateOpinion'
    ),
    path(
        'api/v1.0/product/opinion/list/',
        views.GetOpinionesDeProduct.as_view(),
        name='GetOpinionesDeProduct'
    ),
    path(
        'api/v1.0/product/opinion/user/',
        views.GetUserOpinion.as_view(),
        name='GetUserOpinion'
    ),
    path(
        'api/v1.0/product/opinion/user/delete/<pk>',
        views.DeleteUserOpinion.as_view(),
        name='DeleteUserOpinion'
    ),
    path(
        'api/v1.0/product/opinion/user/update/<pk>',
        views.UpdateUserOpinion.as_view(),
        name='UpdateUserOpinion'
    ),
    path(
        'api/v1.0/product/categories/marcas/',
        views.MarcasOnCategories.as_view(),
        name='MarcasOnCategories'
    ),
    path(
        'api/v1.0/product/categories/marcas/filter/',
        views.FilterByMarca.as_view(),
        name='FilterByMarca'
    ),


    


    

    ######Preguntas

    path(
        'api/v1.0/product/question/list/',
        views.PreguntasList.as_view(),
        name='PreguntasList'
    ),
    path(
        'api/v1.0/product/question/create/',
        views.PreguntaCreate.as_view(),
        name='PreguntaCreate'
    ),
    path(
        'api/v1.0/product/question/count/',
        views.CountNewsCuestions.as_view(),
        name='CountNewsCuestions'
    ),
    path(
        "api/v1.0/admin/questions/news/",
        views.GetNewsQuestionsOffTienda.as_view(),
        name="GetNewsQuestionsOffTienda",
    ),
    path(
        "api/v1.0/admin/questions/update/<pk>",
        views.UpdateQuestion.as_view(),
        name="UpdateQuestion",
    ),
    path(
        'api/v1.0/admin/product/question/novistas/',
        views.ClearProductQuestionsNoVistas.as_view(),
        name='ClearProductQuestionsNoVistas'
    ),
    path(
        'api/v1.0/admin/product/question/delete/<pk>',
        views.DeleteQuestion.as_view(),
        name='DeleteQuestion'
    ),


    ######Preguntas
    
    
    ####### CATEGORIES ##########
    path(
        'api/v1.0/categories/list/',
        views.ListCategoriesParent.as_view(),
        name='ProductsSearch'
    ),
    path(
        'api/v1.0/subcategories/list/',
        views.ListSubCategories.as_view(),
        name='ProductsSearch'
    ),
    path(
        'api/v1.0/subcategories/inverse/list/',
        views.ListSubCategoriesInverse.as_view(),
        name='ProductsSearch'
    ),
    path(
        'api/v1.0/category/detail/<pk>',
        views.CategoryDetailView.as_view(),
        name='ListProductsSalints'
    ),
    path(
        'api/v1.0/category/product/list/',
        views.GetProductsOfCategory.as_view(),
        name='ListProducts'
    ),
    path(
        'api/v1.0/oncategory/product/list/',
        views.SearchProductOnCategory.as_view(),
        name='SearchProductOnCategory'
    ),
    path(
        'api/v1.0/category/search/',
        views.SearchCategoryWithTgr.as_view(),
        name='ListProductsSalints'
    ),
    path(
        'api/v1.0/oncategory/search/icontains/',
        views.SearchProductOnCategoryIcontains.as_view(),
        name='ListProductsSalints'
    ),
    path(
        "api/v1.0/tienda/search/product/categories/subcategories/",
        views.HasSubCategories.as_view(),
        name="HasSubCategories",
    ),
    path(
        "api/v1.0/tienda/search/product/categories/subcategories/",
        views.HasSubCategories.as_view(),
        name="HasSubCategories",
    ),
    path(
        "api/v1.0/tienda/categories/list/",
        views.ListCategories.as_view(),
        name="ListCategories",
    ),

    

    

    #######CATEGORIAS##################

    ########CATEGORIAS ADMIN#################
    path(
        'api/v1.0/admin/categories/',
        views.GetCateogiesPrivate.as_view(),
        name='AdminGetCategories'
    ),
    path(
        'api/v1.0/admin/categorie/create',
        views.AddPrincipalCategoria.as_view(),
        name='AdminCreateCategoria'
    ),
    path(
        'api/v1.0/admin/categorie/delete/<pk>/',
        views.DeleteCategoria.as_view(),
        name='AdminDeleteCategoria'
    ),
    path(
        'api/v1.0/admin/categorie/update/<pk>/',
        views.UpdateCategoria.as_view(),
        name='AdminDeleteCategoria'
    ),

    ########CATEGORIAS ADMIN#################
    

    ########PRODUCTOS ADMIN#################

    path(
        'api/v1.0/admin/category/product/list/',
        views.GetProductsOfCategoryPrivate.as_view(),
        name='ListProductsPrivate'
    ),


    path(
        'api/v1.0/admin/product/view/<pk>',
        views.ProductDetailViewAdmin.as_view(),
        name='AdminViewProduct'
    ),


    path(
        'api/v1.0/admin/product/create',
        views.CreateProduct.as_view(),
        name='AdminCreateProduct'
    ),

    path(
        'api/v1.0/admin/product/delete/<pk>/',
        views.DeleteProduct.as_view(),
        name='AdminDeleteProduct'
    ),
    path(
        'api/v1.0/admin/product/update/<pk>/',
        views.UpdateProduct.as_view(),
        name='AdminCreateProduct'
    ),
    
    path(
        'api/v1.0/admin/product/public/<pk>/',
        views.UpadatePublicStatusProduct.as_view(),
        name='AdminCreateProduct'
    ),
    path(
        'api/v1.0/admin/product/search/category/',
        views.SearchProduct.as_view(),
        name='ProductsSearch'
    ),

    path(
        'api/v1.0/admin/product/images/<int:product>',
        views.GetImagesOffProduct.as_view(),
        name='GetImagesOffProduct'
    ),
    path(
        'api/v1.0/admin/product/images/count/',
        views.CantImagesOffProduct.as_view(),
        name='GetImagesOffProduct'
    ),


    
    path(
        'api/v1.0/admin/product/image/<pk>',
        views.EditProductPortadaImage.as_view(),
        name='GetImagesOffProduct'
    ),
    path(
        'api/v1.0/admin/product/edit/images/<pk>',
        views.EditProductImages.as_view(),
        name='AdminEditProductImages'
    ),

    path(
        'api/v1.0/admin/product/delete/images/<pk>',
        views.DeleteProductImages.as_view(),
        name='AdminDeleteProductImages'
    ),
    
    #upload multiple images
    path(
        'api/v1.0/admin/product/images',
        views.CreateMoreProductImages.as_view(),
        name='CreateEntryImages'
    ),

    ################VARIACIONES######################
    path(
        'api/v1.0/admin/product/variations/search/',
        views.BuscarVariaciones.as_view(),
        name='AdminCreateProduct'
    ),

    path(
        'api/v1.0/admin/product/atributos/',
        views.ListAtributosWithItemsforProduct.as_view(),
        name='AdminListAtributosWithItemsforProduct'
    ),
    path(
        'api/v1.0/admin/product/variation/<pk>',
        views.ListVariacionEncontrdas.as_view(),
        name='AdminListVariacionEncontrdas'
    ),
    path(
        'api/v1.0/admin/product/variation/type/update/<pk>',
        views.HasVariationOnlyAttributeUpdate.as_view(),
        name='HasVariationOnlyAttributeUpdate'
    ),

    ##########Crear/eliminar/modificar ATRIBUTOS#########################

    path(
        'api/v1.0/admin/product/atributo/create',
        views.CreateAtributo.as_view(),
        name='AdminDeleteAtributo'
    ),

    path(
        'api/v1.0/admin/product/atributo/delete/<pk>/',
        views.DeleteAtributoDelProducto.as_view(),
        name='AdminDeleteAtributo'
    ),

    path(
        'api/v1.0/admin/product/atributo/item/create',
        views.CreateItemAtributo.as_view(),
        name='AdminCreateItemAtributo'
    ),
    path(
        'api/v1.0/admin/atributo/item/<int:item>',
        views.GetItem.as_view(),
        name='AdminCreateItemAtributo'
    ),
    
    
    

    ######################variaciones#########################

    #lista variaciones por producto
    path(
        'api/v1.0/admin/product/variation/view/',
        views.GetVariationsOffProduct.as_view(),
        name='AdminCreateItemAtributo'
    ),
    path(
        'api/v1.0/admin/product/variation/min/<int:product>',
        views.MinPriceVariacion.as_view(),
        name='AdminCreateItemAtributo'
    ),
    path(
        'api/v1.0/admin/product/variation/detail/',
        views.GetProductAndVariacionForOrderDetail.as_view(),
        name='AdminGetProductAndVariacionForOrderDetail'
    ),
    path(
        'api/v1.0/admin/variation/delete/<pk>',
        views.DeleteVariacion.as_view(),
        name='DeleteVariacion'
    ),
    path(
        'api/v1.0/admin/variation/update/<pk>',
        views.UpdateVariacion.as_view(),
        name='UpdateVariacion'
    ),




    ########PRODUCTOS ADMIN#################

]