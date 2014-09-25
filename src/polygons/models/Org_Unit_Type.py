from django.db import models

class Org_Unit_Type(models.Model):
    
    name = models.TextField(unique=True)
    
    class Meta:
        app_label = 'polygons'