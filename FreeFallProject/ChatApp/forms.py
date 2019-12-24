from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
from django import forms
from django.core.files import File
from .models import Photo

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

        
class HikeForm(forms.Form):

    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=200000)# ,validators=[validators.])
    short_description = forms.CharField(max_length=1000)

    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
   
    coordinates = forms.CharField(max_length=200000)


