from django import forms
from django.contrib.auth.models import User


class EditProfile(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AuthCodeForm(forms.Form):
    code = forms.IntegerField(label='Код регистрации')
