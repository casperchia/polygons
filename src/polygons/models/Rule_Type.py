from django.db import models

class Rule_Type(models.Model):
    
    name = models.TextField(unique=True)
    abbreviation = models.CharField(max_length=2, unique=2)
    
    class Meta:
        app_label = 'polygons'