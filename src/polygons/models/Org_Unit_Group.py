from django.db import models

from Org_Unit import Org_Unit

class Org_Unit_Group(models.Model):
    
    owner = models.ForeignKey(Org_Unit, on_delete=models.PROTECT)
    member = models.ForeignKey(Org_Unit, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'