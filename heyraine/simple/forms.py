from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(label='Your email', max_length=100,required=True,widget=forms.TextInput(attrs={'class':'form-control','style' : 'height:5vh'}) )
class StartForm(forms.Form):
    start = forms.CharField(label='start', max_length=100,required=True,widget=forms.TextInput(attrs={'class':'form-control','style' : 'height:5vh'}) )
