from django import forms
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    #template_name='/something/else'

    class Meta:
        model = User
        fields = (
        	'username',
            'first_name',
            'last_name',
            'email',  
        )
