from django.db import models

from Org_Unit import Org_Unit

class Org_Unit_Group(models.Model):
    
    owner = models.ForeignKey(Org_Unit, on_delete=models.PROTECT,
                              related_name='owner')
    member = models.ForeignKey(Org_Unit, on_delete=models.PROTECT,
                               related_name='member')
    
    class Meta:
        app_label = 'polygons'
        unique_together = ['owner', 'member']