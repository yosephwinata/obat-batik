from django import forms

from .models import Supplier

# class ReviewForm(forms.Form):
#     user_name = forms.CharField(label="Your Name", max_length=100, error_messages={
#         "required": "Your name must not be empty!",
#         "max_length": "Please enter a shorter name!"
#     })
#     review_text = forms.CharField(label="Your Feedback", widget=forms.Textarea, max_length=200)
#     rating = forms.IntegerField(label="Your Rating", min_value=1, max_value=5)

class SupplierForm(forms.Form):
    name = forms.CharField(label='Nama*', max_length=70, error_messages={
        'required': 'Nama harus diisi',
        'max_length': 'Nama terlalu panjang'
    }, widget= forms.TextInput(attrs={
        'class':'form-control',
		'autofocus': True,
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix