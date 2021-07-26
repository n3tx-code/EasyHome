from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User


class SignInForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmation mot de passe", required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        labels = {
            'first_name': "Prénom",
            'last_name': "Nom",
            'username': "Pseudo",
            'email': "Adresse mail",
            'password': "Mot de passe",
        }
        widgets = {
            'password': forms.PasswordInput
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', "Inscription"))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            msg = "Mot de passe différents"
            self.add_error('password', msg)
            self.add_error('password2', msg)

        if User.objects.filter(email=cleaned_data.get("email")):
            self.add_error('email', "Email déjà utilisée")

        if User.objects.filter(username=cleaned_data.get("username")):
            self.add_error('username', "Pseudo déjà utilisé")
