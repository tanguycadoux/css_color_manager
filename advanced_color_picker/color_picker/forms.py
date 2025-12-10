from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import inlineformset_factory

from .models import Color


class ColorInterpolationForm(forms.Form):
    l_min = forms.FloatField(min_value=0, max_value=1)
    l_max = forms.FloatField(min_value=0, max_value=1)

    c_min = forms.FloatField(min_value=0, max_value=1)
    c_max = forms.FloatField(min_value=0, max_value=1)

    h_min = forms.FloatField(min_value=0, max_value=360)
    h_max = forms.FloatField(min_value=0, max_value=360)

    count = forms.IntegerField(min_value=2, max_value=10)
