from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



def validate_hike_name(value):
    if len(value)<3:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
class HikeForm(forms.Form):

    name = forms.CharField(max_length=200, validators=[validate_hike_name])
    description = forms.CharField(max_length=200000)# ,validators=[validators.])
    short_description = forms.CharField(max_length=1000)

    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
   
    coordinates = forms.CharField(max_length=200000)


