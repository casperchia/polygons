from django.db import models

class Subject_Area(models.Model):

    code = models.CharField(max_length=4, unique=True)
    name = models.TextField()
    
    def __unicode__(self):
        return '%s: %s'%(self.code, self.name)
        
    class Meta:
        app_label = 'polygons'
