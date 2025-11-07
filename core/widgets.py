from django import forms

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True