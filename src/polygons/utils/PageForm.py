from django import forms

class PageForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput, required=True)
