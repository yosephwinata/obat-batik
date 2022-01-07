from django import forms

from .models import Ingredient

class IngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix

    class Meta:
        model = Ingredient
        fields = ['name']
        labels = {
            'name': 'Nama*'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'autofocus': True
            })
        }
        error_messages = {
            'name': {
                'max_length': 'Nama terlalu panjang',
                'unique': 'Nama sudah terdaftar'
            }
        }