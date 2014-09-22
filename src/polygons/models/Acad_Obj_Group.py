from django.db import models

from Acad_Obj_Group_Type import Acad_Obj_Group_Type

class Acad_Obj_Group(models.Model):
    
    name = models.TextField()
    type = models.ForeignKey(Acad_Obj_Group_Type, on_delete=models.PROTECT)
    enumerated = models.BooleanField(default=False)
    parent = models.OneToOneField('self', on_delete=models.PROTECT)
    definition = models.TextField(null=True)
    
    class Meta:
        app_label = 'polygons'