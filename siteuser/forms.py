"""Forms"""

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.widgets import ClearableFileInput

from .models import SiteUser, Role, Message

CustomUser = get_user_model()

class UserCreationForm(forms.ModelForm):
    """Custom UCF. Takes the standard
    variables of 'email', 'password1', 'password2'
    For creating instances of 'CustomUser'."""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = CustomUser
        fields = ["email", "password", "is_active", "is_admin"]

    def clean_password(self):
        return self.initial["password"]

class SiteUserMixin(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ("screen_name", )
        widgets = {
            "screen_name" : forms.TextInput(attrs={'class':'form-control', "placeholder" : "Display name"}),
        }

class SiteUserRegistrationForm(forms.Form):
    agreement = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput())

    screen_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', "placeholder" : "Screen name (maximum of 20 characters)"}))

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', "placeholder" : "Email address"}))

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Verify password"}))

    def clean(self):
        data = self.cleaned_data

        try:
            email = data.get("email", None).strip()
        except AttributeError:
            self.add_error('email', 'Email field is required')

        try:
            password1 = data.get('password1', None).strip()
        except AttributeError:
            self.add_error('password1', 'Please provide a password')

        try:
            password2 = data.get('password2', None).strip()
        except AttributeError:
            self.add_error('password2', 'Please provide a confirmation password')

        try:
            screen_name = data.get("screen_name", None).strip()
        except AttributeError:
            self.add_error('screen_name', 'Display name field is required')

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already registered.')

        if password1 and password2 and password1 != password2:
            self.add_error('password1', "Passwords do not match")

        if SiteUser.objects.filter(screen_name=screen_name).exists():
            self.add_error('screen_name', 'Display name already taken.')

class SiteUserEditForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ["first_name", "last_name", "location", "avatar", "roles"]

        widgets = {
            "first_name" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "First name (maximum of 20 characters)"}),
            "last_name" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Last name (maximum of 20 characters)"}),
            "location" : forms.TextInput(attrs={'class' : 'form-control', "placeholder" : "Location (maximum of 50 characters)"}),
            "roles" : AddAnotherWidgetWrapper(
                forms.SelectMultiple(attrs={'class' : 'form-control'}),
                reverse_lazy('siteuser:role_create')),
            'avatar' : ClearableFileInput(attrs={'class' : 'form-control', 'accept' : '.png, .PNG, .jpg, .JPG, .jpeg, .JPG'}),
        }

    def clean_location(self):
        location = self.cleaned_data['location']
        try:
            return location.lower().strip()
        except AttributeError:
            return ''

class PassWordGetterForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data['password']
        if check_password(password, self.user.password) is False:
            self.add_error('password', 'You entered a wrong password')

class EmailAndPassWordGetterForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control', 'type':'password', "placeholder" : "Enter password"}))

class NewRoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ("name", )

        widgets = {
            "name" : forms.TextInput(
                attrs={'class' : 'form-control', "placeholder" : "Role"})
        }

    def clean(self):
        name = self.cleaned_data.get("name", None).lower().strip()
        if Role.objects.filter(name=name):
            self.add_error('name', "Role with this name already exists")

class RoleEditForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ("name", )

        widgets = {
            "name" : forms.TextInput(
                attrs={'class' : 'form-control', "placeholder" : "Role"})
        }
