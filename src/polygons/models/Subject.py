from django.db import models

from Org_Unit import Org_Unit
from Career import Career
from Acad_Obj_Group import Acad_Obj_Group

class Subject(models.Model):
    
    code = models.CharField(max_length=8, unique=True)
    name = models.TextField()
    uoc = models.PositiveIntegerField()
    offered_by = models.ForeignKey(Org_Unit, on_delete=models.PROTECT,
                                   null=True)
    career = models.ForeignKey(Career, on_delete=models.PROTECT)
    excluded = models.ForeignKey(Acad_Obj_Group, on_delete=models.PROTECT,
                                 null=True)
    
    
    class Meta:
        app_label = 'polygons'