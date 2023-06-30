from django.db import models

class EntryManager(models.Manager):
    
    def GetAllEntries(self,tienda):
        return self.filter(
            tienda=tienda,
            public=True,
            portada=True,
        ).order_by('created')[:10]