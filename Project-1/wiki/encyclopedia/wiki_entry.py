from django import forms
from django.forms.widgets import Textarea


class WikiEntry(forms.Form):
    title = forms.CharField(
        label="Wiki Entry Title",
        widget=forms.TextInput(attrs={'class': "form-control"}))
    entry_body = forms.CharField(
        widget=Textarea(attrs={'class': "form-control"}),
        label="Wiki Entry Body")
