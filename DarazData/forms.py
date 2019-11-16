from django.forms import ModelForm
from .models import Contact

class ContactForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Contact
        fields = '__all__'


