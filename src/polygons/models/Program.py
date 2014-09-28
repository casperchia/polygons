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
    uoc = models.PositiveIntegerField()
    
    def __unicode__(self):
        return '%s (%s)'%(self.name, str(self.degree))
    
    @property
    def handbook_link(self):
        return 'http://www.handbook.unsw.edu.au/%s/programs/2015/%s.html'%(
                    self.career.name, self.code)
    
    class Meta:
        app_label = 'polygons'
