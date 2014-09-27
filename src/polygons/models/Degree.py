from django.db import models

class Degree(models.Model):
    
    name = models.TextField(unique=True)
    abbreviation = models.TextField()
    
    class Meta:
        app_label = 'polygons'