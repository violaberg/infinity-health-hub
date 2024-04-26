from django.forms import ModelForm
from .models import Contact


class ContactForm(ModelForm):
    """
    A form to allow users to contact the site owner
    """
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email',

            'message': 'Message',

        }

        self.fields['email'].widget.attrs['autofocus'] = True
