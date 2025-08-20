from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from apps.project.models import Designer


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(
            attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(
            attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
    )


class EmailForm(forms.Form):
    CHOICES = [
        ('Area progetti', 'Area progetti'),
        ('Area amministrazione', 'Area amministrazione'),
        ('Area profilo personale', 'Area profilo personale'),
        ('Area tecnica', 'Area tecnica'),
        ('Altro', 'Altro'),
    ]

    dropdown = forms.ChoiceField(choices=CHOICES)
    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Problema riscontrato'
    }))
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
        'placeholder': 'Descrizione',
        'rows': 5
    }))


class DesignerForm(forms.ModelForm):
    class Meta:
        model = Designer
        fields = ['logo']
