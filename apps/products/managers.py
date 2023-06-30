from django.db import models
#busque trigram postgres
from django.contrib.postgres.search import TrigramSimilarity

class ProductManager(models.Manager):
    
    def producto_destacado(self,tienda):
        return self.filter(
            tienda=tienda,
            public = True,
            portada=True
        ).order_by('-created')[:10]

    def producto_en_ofertas(self,tienda):
        return self.filter(
            tienda=tienda,
            public=True,
            in_offer=True,
        ).order_by('-created')[:10]

    def producto_nuevos(self,tienda):
        return self.filter(
            tienda=tienda,
            public=True,
        ).order_by('-created')[:12]

    def search_product_trg(self,kword,tienda):
        
            return self.filter(
                tienda=tienda,
                title__trigram_similar=kword,
                public = True,
            )
      
    def search_product_on_category_trg(self,kword,tienda,category):
        if kword:
            return self.filter(
                tienda=tienda,
                title__trigram_similar=kword,
                category = category,
            )
        else:
            return self.filter(
                tienda=tienda,
                category=category,
            )

    def search_product_icontais(self,kword,tienda):
        return self.filter(
            tienda=tienda,
            title__icontains = kword,
            public = True
        )
       
    def search_product_icontais_on_category(self,kword,tienda,category):
        return self.filter(
            tienda=tienda,
            title__icontains = kword,
            category = category
        )
    
    def GetProductsOfCategory(self,kword):
            return self.filter(
                category=kword,       
            )

    def GetProductsOfCategoryPrivate(self,kword,tienda):
            return self.filter(
                category=kword,
                tienda=tienda,       
            )

    def search_product_trgOnCategory(self,kword,Kwordctg):
            return self.filter(
                title__trigram_similar=kword,
                category=Kwordctg,
                public = True,
            )
       
    
    def search_product_IcontainsOnCategory(self,kword,Kwordctg):
        if kword:
            return self.filter(
                title__icontains=kword,
                category=Kwordctg,
                public = True,
            )
        else:
            return self.filter(
                category=Kwordctg,
            )[:10]

    """ FILTROS """

    def Filer_product_cheap(self,Kwordctg):
            return self.filter(
                category=Kwordctg,       
            ).order_by('price')

    def Filer_product_on_offert(self,Kwordctg):
            return self.filter(
            category=Kwordctg,
            in_offer=True,       
            ).order_by('price')

class CategoryManager(models.Manager):
    
    def categories_parent(self,tienda):
        return self.filter(
            tienda=tienda,
            parent =None
        )

    def search_category_trg(self,kword,tienda):
            return self.filter(
                tienda=tienda,
                name__trigram_similar=kword,
            )




#####################VARIACIONES##############################
class AtributoManager(models.Manager):
    
    def AtributosWithItemForProduct(self,kword):
        return self.filter(
            product = kword
        )


#####################VARIACIONES##############################


