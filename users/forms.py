from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,\
    PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional')
    email = forms.CharField(max_length=254, validators=[EmailValidator])

    class Meta(UserCreationForm):
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        return email.lower()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', validators=[EmailValidator])

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("This user is inactive")


class CustomEmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.CharField(max_length=254, validators=[EmailValidator])

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email, is_active=False):
            raise ValidationError("This user is inactive")
        else:
            if not User.objects.filter(email=email, is_active=True).exists():
                raise ValidationError("No such user exists")
            return email
