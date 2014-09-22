from django.db import models

from Subject import Subject
from Career import Career
from Rule import Rule

class Subject_Prereq(models.Model):
    
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    career = models.ForeignKey(Career, on_delete=models.PROTECT)
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'