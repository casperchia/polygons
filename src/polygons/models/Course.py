from django.db import models

from Subject import Subject
from Semester import Semester

class Course(models.Model):
    
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = [subject, semester]