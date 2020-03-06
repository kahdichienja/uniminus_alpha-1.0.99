from django import forms
from stuff.models import HodProfile, Unit
class HodProfileForm(forms.ModelForm):
    """Form definition for HodProfile."""

    class Meta:
        """Meta definition for HodProfileform."""

        model = HodProfile
        fields = ['school', 'department']

class UnitForm(forms.ModelForm):
    """Form definition for Unit."""
    unit_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'unit_name','required': 'true'}))
    unit_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'unit_code','required': 'true'}))

    class Meta:
        """Meta definition for Unitform."""

        model = Unit
        fields = ['unit_name', 'unit_code']
