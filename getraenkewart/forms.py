from django import forms
from django.contrib.auth.models import User

PASSWORDS_NOT_MATCHING_ERROR = "Passwörter stimmen nicht überein."
PASSWORDS_TOO_SHORT_ERROR = "Passwort muss mindestens 8 Zeichen lang sein."
USERNAME_EXISTS_ERROR = "Der Benutzername existiert bereits."

class EightCharField(forms.CharField):

    def validate(self, value):
        super(EightCharField, self).validate(value)
        if len(value) < 8:
            raise forms.ValidationError(PASSWORDS_TOO_SHORT_ERROR)

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="Vorname",
            widget = forms.TextInput(attrs = {
                "class":"form-control",
                "placeholder":"Vorname",
            }))
    last_name = forms.CharField(max_length=30, label="Nachname",
            widget = forms.TextInput(attrs = {
                "class":"form-control",
                "placeholder":"Nachname",
            }))
    username = forms.CharField(max_length=30, label="Benutzername",
            widget = forms.TextInput(attrs = {
                "class":"form-control",
                "placeholder":"Benutzername",
            }))
    email = forms.EmailField(label="E-mail",
            widget = forms.EmailInput(attrs = {
                "class":"form-control",
                "placeholder":"E-mail",
            }))
    password = EightCharField(label="Passwort",
            widget=forms.PasswordInput(attrs = {
                "class":"form-control",
                "placeholder":"Passwort",
            }))
    password2 = forms.CharField(label="Passwort bestätigen",
            widget=forms.PasswordInput(attrs = {
                "class":"form-control",
                "placeholder":"Passwort bestätigen",
            }))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if User.objects.filter(username__exact=username).exists():
            raise forms.ValidationError(USERNAME_EXISTS_ERROR)
        if password != password2:
            raise forms.ValidationError(PASSWORDS_NOT_MATCHING_ERROR)
        return cleaned_data
