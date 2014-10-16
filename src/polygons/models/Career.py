from django.db import models

class Career(models.Model):
    
    abbreviation = models.CharField(max_length=2, unique=True)
    name = models.TextField(unique=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'polygons'