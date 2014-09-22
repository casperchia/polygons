from django.db import models

from Rule_Type import Rule_Type
from Acad_Obj_Group import Acad_Obj_Group

class Rule(models.Model):
    
    name = models.TextField(null=True)
    type = models.ForeignKey(Rule_Type, on_delete=models.PROTECT)
    min = models.PositiveIntegerField(null=True)
    max = models.PositiveIntegerField(null=True)
    acad_obj_group = models.ForeignKey(Acad_Obj_Group, on_delete=models.PROTECT)
    description = models.TextField(null=True)
    
    class Meta:
        app_label = 'polygons'