from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from assets_auth.models import User


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        strip=False,
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        widget=forms.PasswordInput(),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'email',
                'password1',
                'password2',
            ),
            Submit('submit', 'Cadastrar', css_class='btn-login btn btn-block'),
        )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'As senhas não são iguais.')

        try:
            password_validation.validate_password(password1, self.instance)
        except ValidationError as error:
            self.add_error('password1', error)

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
