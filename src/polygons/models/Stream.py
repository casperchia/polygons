from django.db import models

class Stream(models.Model):
    
    name = models.TextField()
    code = models.CharField(max_length=6, unique=True)
    description = models.TextField(null=True)
    
    class Meta:
        app_label = 'polygons'