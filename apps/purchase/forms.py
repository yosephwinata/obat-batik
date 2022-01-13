from django import forms

from apps.supplier.models import Supplier

from .models import Purchase

class PurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix
        self.fields['supplier'].queryset = Supplier.objects.all().order_by('name')

    class Meta:
        model = Purchase
        fields = ['datetime', 'supplier', 'invoice_number', 'notes']
        labels = {
            'datetime': 'Tanggal*',
            'invoice_number': 'No Invoice',
            'supplier': 'Supplier',
            'notes': 'Catatan'
        }
        widgets = {
            'datetime': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'invoice_number': forms.TextInput(attrs={
                'class':'form-control'
            }),
            'supplier': forms.Select(attrs={
                'class':'form-control'
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