from django.db import models

from Org_Unit import Org_Unit
from Career import Career
from Degree import Degree

class Program(models.Model):
    
    name = models.TextField()
    code = models.CharField(max_length=4, unique=True)
    offered_by = models.ForeignKey(Org_Unit, on_delete=models.PROTECT,
                                   null=True)
    career = models.ForeignKey(Career, on_delete=models.PROTECT)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True)
    
    def __unicode__(self):
        # Can we please implement this to return a string of the form (without
        # the quotes):
        #    "Software Engineering (Bachelor of Engineering - BE)"
        raise Exception
    
    class Meta:
        app_label = 'polygons'
