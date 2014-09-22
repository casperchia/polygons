from django.db import models

from Subject import Subject
from Acad_Obj_Group import Acad_Obj_Group

class Subject_Group_Member(models.Model):
    
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    acad_obj_group = models.ForeignKey(Acad_Obj_Group, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = [subject, acad_obj_group]