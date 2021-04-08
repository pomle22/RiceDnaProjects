from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

# Create Login form in django form
class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
    widget=forms.TextInput(attrs={'class': 'form-control form-control-lg text-white','type': 'text','id':'username-input'}))
    password = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg text-white','type': 'password','id':'password-input'}))
            
    def __int__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)  

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                raise forms.ValidationError(_("Please confirm your email."))
        else:
            raise forms.ValidationError(_("Invalid username or password."))
        return self.cleaned_data


    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-4'
        }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() == 0:
            raise forms.ValidationError(_('Invalid email'))
        return email


class ResetChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'password', 'class': 'form-control mb-4'
        }))
    password2 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'password', 'class': 'form-control mb-4'
        }))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(_("The password didn't match"))

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password0 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'password','class':'form-control mb-4'
        }))
    password1 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'password','class':'form-control mb-4'
        }))
    password2 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'type': 'password','class':'form-control mb-4'
        }))

    def __int__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(_("The password didn't match"))

        return self.cleaned_data


# Create Signup form
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control white-text'
        }))
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control white-text'
        }))
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control white-text'
        }))
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control white-text'
        }))
    password1 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'class': 'form-control white-text'
            }))
    password2 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': 'password',
                'class': 'form-control mb-4'
            }))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1',
                  'password2', 'email')

    def clean_email(self):
        username = self.cleaned_data.get('username') 
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(
                username=username).count():
            raise forms.ValidationError(_('This email is already used'))
        return email

