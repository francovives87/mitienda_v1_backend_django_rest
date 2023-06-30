from django.urls import path, re_path
from . import views

app_name = 'blog_app'

urlpatterns = [
    #####public
    path(
        'api/v1.0/blog/entry/list/<pk>',
        views.EntryList.as_view(),
        name='EntryList'
    ),
    path(
        'api/v1.0/blog/entry/all/',
        views.GetAllEntriesForBlog.as_view(),
        name='GetAllEntriesForBlog'
    ),
    path(
        'api/v1.0/blog/categories/all/',
        views.GetAllEntryCategories.as_view(),
        name='GetAllEntryCategories'
    ),
    path(
        'api/v1.0/blog/entry/by/categorie/',
        views.GetEntryByCategorie.as_view(),
        name='GetEntryByCategorie'
    ),


    
  

    


    path(
        'api/v1.0/blog/view/<pk>',
        views.TiendaEntryDetailPublic.as_view(),
        name='EntryDetail'
    ),
    ##################  PRIVATE  ###################
    
    ############CATEGORIAS #######################
    path(
        'api/v1.0/admin/blog/categories/',
        views.GetCategoriesOffTienda.as_view(),
        name='ListBlogCategoriesPrivate'
    ),
    path(
        'api/v1.0/admin/blog/category/update/<pk>',
        views.UpdateCategory.as_view(),
        name='UpdateBlogCategory'
    ),
    path(
        'api/v1.0/admin/blog/category/delete/<pk>',
        views.DeleteCategoryPrivate.as_view(),
        name='DeleteBlogCategory'
    ),


    ##################ENTRADAS ##############################

    path(
        'api/v1.0/admin/blog/entry/',
        views.GetEntrysOffCategory.as_view(),
        name='ListBlogCategoriesPrivate'
    ),
    path(
        'api/v1.0/admin/blog/category/create',
        views.CreateCategoryBlogPrivate.as_view(),
        name='CreateBlogCategory'
    ),
    path(
        'api/v1.0/admin/blog/entry/create',
        views.CreateEntryPrivate.as_view(),
        name='CreateBlogEntry'
    ),

    path(
        'api/v1.0/admin/blog/entry/images',
        views.CreateEntryImages.as_view(),
        name='CreateEntryImages'
    ),
    path(
        'api/v1.0/admin/blog/entry/delete/<pk>',
        views.DeleteEntryPrivate.as_view(),
        name='DeleteEntryImages'
    ),
    path(
        'api/v1.0/admin/blog/entry/public/<pk>/',
        views.EntryPublicUpdate.as_view(),
        name='AdminCreateSlider'
    ),
    path(
        'api/v1.0/admin/blog/entry/portada/<pk>/',
        views.EntryPortadaUpdate.as_view(),
        name='AdminCreateSlider'
    ),

    
    path(
        'api/v1.0/admin/blog/entry/content/update/<pk>/',
        views.EntryUpdateContent.as_view(),
        name='AdminEntryContentUpdate'
    ),
    path(
        'api/v1.0/admin/blog/entry/view/<pk>',
        views.TiendaEntryDetail.as_view(),
        name='EntryDetail'
    ),
    path(
        'api/v1.0/admin/blog/entry/images/count/',
        views.CantImagesOffProduct.as_view(),
        name='EntryDetail'
    ),
    path(
        'api/v1.0/admin/blog/entry/update/portada/<pk>',
        views.EditEntryPortadaImage.as_view(),
        name='EntryDetail'
    ),
    path(
        'api/v1.0/admin/blog/entry/update/images/<pk>',
        views.EditEntryImages.as_view(),
        name='EntryDetail'
    ),
    path(
        'api/v1.0/admin/blog/entry/delete/images/<pk>',
        views.DeleteEntryImages.as_view(),
        name='EntryDetail'
    ),
    ###COMMENTS

    path(
        'api/v1.0/blog/entry/comments/',
        views.ListComments.as_view(),
        name='ListComments'
    ),
    path(
        'api/v1.0/blog/entry/comments/parent/create/',
        views.CreateCommentParent.as_view(),
        name='CreateCommentParent'
    ),
    path(
        'api/v1.0/blog/entry/comments/children/create/',
        views.CreateCommentResponse.as_view(),
        name='CreateCommentResponse'
    ),


    
    
]