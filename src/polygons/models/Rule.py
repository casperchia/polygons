from django.db import models

from Rule_Type import Rule_Type
from Enumeration_Type import Enumeration_Type

class Rule(models.Model):
    
    name = models.TextField(null=True)
    type = models.ForeignKey(Rule_Type, on_delete=models.PROTECT)
    min = models.PositiveIntegerField(null=True)
    max = models.PositiveIntegerField(null=True)
    enumeration_type = models.ForeignKey(Enumeration_Type,
                                         on_delete=models.PROTECT, null=True)
    enumerated = models.BooleanField()
    parent = models.OneToOneField('self', on_delete=models.PROTECT, null=True)
    definition = models.TextField(null=True)
    
    class Meta:
        app_label = 'polygons'