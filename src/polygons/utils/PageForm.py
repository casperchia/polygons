from django import forms

class PageForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput, required=True)

