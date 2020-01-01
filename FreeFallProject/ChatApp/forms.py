from django import forms
from django.core import validators

class HikeForm(forms.Form):

    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=200000)# ,validators=[validators.])
    short_description = forms.CharField(max_length=1000)

    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
   
    coordinates = forms.CharField(max_length=200000)
from django.contrib.auth.forms import UserCreationForm

