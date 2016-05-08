from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(label='Your email', max_length=100)
