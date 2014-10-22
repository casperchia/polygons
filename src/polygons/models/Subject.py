from django.db import models

from Org_Unit import Org_Unit
from Career import Career
from Acad_Obj_Group import Acad_Obj_Group
from Subject_Area import Subject_Area

class Subject(models.Model):
    
    code = models.CharField(max_length=8, unique=True)
    name = models.TextField()
    uoc = models.PositiveIntegerField()
    subject_area = models.ForeignKey(Subject_Area, on_delete=models.PROTECT)
    offered_by = models.ForeignKey(Org_Unit, on_delete=models.PROTECT,
                                   null=True)
    career = models.ForeignKey(Career, on_delete=models.PROTECT)
    excluded = models.ForeignKey(Acad_Obj_Group, on_delete=models.PROTECT,
                                 null=True)
    
    def __unicode__(self):
        return '%s (%s)'%(self.code, self.name)
        
    @property
    def handbook_link(self):
        return 'http://www.handbook.unsw.edu.au/%s/courses/2013/%s.html'%(
                    self.career.name, self.code)
    
    class Meta:
        app_label = 'polygons'
