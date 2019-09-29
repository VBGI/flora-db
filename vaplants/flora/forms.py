from django import forms
from flora.models import RarityMixin


class FilterForm(forms.Form):
    rarity = forms.ChoiceField(choices=RarityMixin.RARITY_CHOICES,
                               required=False)
    query = forms.CharField(max_length=50, required=False)
    reverse = forms.BooleanField(required=False)

