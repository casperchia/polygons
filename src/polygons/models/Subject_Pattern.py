from django.db import models

class Subject_Pattern(models.Model):
    
    pattern = models.TextField(unique=True)
    
    class Meta:
        app_label = 'polygons'