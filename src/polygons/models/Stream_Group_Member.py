from django.db import models

from Stream import Stream
from Acad_Obj_Group import Acad_Obj_Group

class Stream_Group_Member(models.Model):
    
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT)
    acad_obj_group = models.ForeignKey(Acad_Obj_Group, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = [stream, acad_obj_group]