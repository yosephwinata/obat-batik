from django import forms

from .models import Adjustment

class AdjustmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix

    class Meta:
        model = Adjustment
        fields = ['datetime', 'notes']
        labels = {
            'datetime': 'Tanggal*',
            'notes': 'Catatan'
        }
        widgets = {
            'datetime': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class':'form-control',
                'rows': 2,
            })
        }
        error_messages = {
            'invoice_number': {
                'max_length': 'No nota terlalu panjang'
            },
            'notes': {
                'max_length': 'Catatan terlalu panjang'
            },
        }