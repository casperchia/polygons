from django.db import models

class Degree(models.Model):
    
    name = models.TextField(unique=True)
    abbreviation = models.TextField()
    
    def __unicode__(self):
        return '%s - %s'%(self.name, self.abbreviation)
    
    class Meta:
        app_label = 'polygons'