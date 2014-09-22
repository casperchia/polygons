from django.db import models

from Stream import Stream
from Rule import Rule

class Stream_Rule(models.Model):
    
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT)
    rule = models.ForeignKey(Rule, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'polygons'
        unique_together = [stream, rule]