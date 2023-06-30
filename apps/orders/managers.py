from django.db import models

class OrderManager(models.Manager):
    
    def ordenes_por_user(self,kword):
        return self.filter(
            user=kword
        ).order_by('-created')

class OrderDetailManager(models.Manager):

    def productos_por_ventas(self, order_id):
        return self.filter(
            order__id=order_id
        ).order_by('-created')



        