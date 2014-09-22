from django.db import models

from Program import Program
from Acad_Obj_Group import Acad_Obj_Group

class Program_Group_Member(models.Model):
    
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    acad_obj_group = models.ForeignKey(Acad_Obj_Group, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = [program, acad_obj_group]