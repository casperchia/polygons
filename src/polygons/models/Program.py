from django.db import models

from Org_Unit import Org_Unit
from Career import Career

class Program(models.Model):
    
    name = models.TextField()
    offered_by = models.ForeignKey(Org_Unit, on_delete=models.PROTECT,
                                   null=True)
    career = models.ForeignKey(Career, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'