from django import forms

from .models import Supplier

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix

    class Meta:
        model = Supplier
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


# class ReviewForm(forms.Form):
#     user_name = forms.CharField(label="Your Name", max_length=100, error_messages={
#         "required": "Your name must not be empty!",
#         "max_length": "Please enter a shorter name!"
#     })
#     review_text = forms.CharField(label="Your Feedback", widget=forms.Textarea, max_length=200)
#     rating = forms.IntegerField(label="Your Rating", min_value=1, max_value=5)
