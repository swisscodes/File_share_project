from django import forms
from django.contrib.auth.models import User
from . models import UploadFile
from django.forms.widgets import Textarea


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']




class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('document', 'record_no', 'file_name', 'description', 'share_status')
        widgets = {
            'description': Textarea()
        }