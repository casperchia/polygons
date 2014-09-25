from django.db import models

class Acad_Obj_Group_Type(models.Model):
    
    name = models.TextField(unique=True)
    
    class Meta:
        app_label = 'polygons'