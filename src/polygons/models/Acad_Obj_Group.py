from django.db import models

from Acad_Obj_Group_Type import Acad_Obj_Group_Type

class Acad_Obj_Group(models.Model):
    
    name = models.TextField(null=True)
    type = models.ForeignKey(Acad_Obj_Group_Type, on_delete=models.PROTECT)
    enumerated = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    definition = models.TextField(null=True)
    logical_or = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'polygons'