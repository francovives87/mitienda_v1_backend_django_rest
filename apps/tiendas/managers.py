from django.db import models
#busque trigram postgres
from django.contrib.postgres.search import TrigramSimilarity

class TiendaManager(models.Manager):

    def GetTiendaManager(self,tienda):
        return self.filter(
            name=tienda
        )[0:1] #solo uno

class SliderManager(models.Manager):

    def GetSliderOffTienda(self,tienda):
        return self.filter(
            tienda=tienda,
            is_public=True
        ).order_by('-created')

class ColorsManager(models.Manager):
    
    def GetColorsOffTienda(self,tienda):
        return self.filter(
            tienda=tienda
        ).order_by('-created')[0:1]