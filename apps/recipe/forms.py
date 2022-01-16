from django import forms

from .models import Recipe

class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix

    class Meta:
        model = Recipe
        fields = ['name', 'notes']
        labels = {
            'name': 'Nama*',
            'notes': 'Catatan'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'autofocus': True
            }),
            'notes': forms.Textarea(attrs={
                'class':'form-control',
                'rows': 2,
            })
        }
        error_messages = {
            'name': {
                'max_length': 'Nama terlalu panjang',
                'unique': 'Nama sudah terdaftar'
            },
            'notes': {
                'max_length': 'Catatan terlalu panjang'
            },
        }