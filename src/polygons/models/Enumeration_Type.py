from django.db import models

class Enumeration_Type(models.Model):
    
    name = models.TextField(unique=True)
    
    class Meta:
        app_label = 'polygons'