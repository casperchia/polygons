from django import forms

from polygons.models.Program_Plan import Program_Plan

class PageForm(forms.ModelForm):
    class Meta:
        model = Program_Plan
