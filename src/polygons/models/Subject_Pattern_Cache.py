from django.db import models

from Subject_Pattern import Subject_Pattern
from Subject import Subject

class Subject_Pattern_Cache(models.Model):
    
    subject_pattern = models.ForeignKey(Subject_Pattern,
                                        on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = ['subject_pattern', 'subject']