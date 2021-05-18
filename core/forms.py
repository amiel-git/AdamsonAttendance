from django.forms import ModelForm
from django import forms
from core.models import User

class RegistrationForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'profile_image'
        ]
        widgets = {
            'email': forms.widgets.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'password': forms.widgets.PasswordInput(attrs={'class':'form-control'}),
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
