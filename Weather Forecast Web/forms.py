from django import forms
from .models import Review
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from pyzipcode import ZipCodeDatabase
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

zdb = ZipCodeDatabase()


class WeatherForm(forms.Form):
    zip_code = forms.CharField(label="ZIP Code:", max_length=5)

    def clean_zip_code(self):
        zip_code = self.cleaned_data["zip_code"]
        try:
            zdb[zip_code]  # this will raise an exception if the zip code is invalid
        except (KeyError, IndexError):
            raise ValidationError(
                "You've made an invalid submission. Please enter a valid ZIP code."
            )
        return zip_code
