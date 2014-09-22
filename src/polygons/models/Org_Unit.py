from django.db import models

from Org_Unit_Type import Org_Unit_Type

class Org_Unit(models.Model):
    
    type = models.ForeignKey(Org_Unit_Type, on_delete=models.PROTECT)
    name = models.TextField()
    
    class Meta:
        app_label = 'polygons'