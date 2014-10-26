from django.db import models

from Subject import Subject
from Rule import Rule

class Subject_Coreq(models.Model):
    
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = ['subject', 'rule']