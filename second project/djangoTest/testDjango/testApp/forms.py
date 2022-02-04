from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField, ChoiceField, PasswordInput
from django.core.exceptions import ValidationError
from django.utils import timezone as tz
from django.contrib import messages
from .models import Recipe, Tag, Ing


def validate_date_not_in_future(value):
    if value > tz.now():
        raise ValidationError('date is in the future')

class PasswordChangingForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ( 'name', 'tag', 'image', 'time', 'dis', 'ing')


class IngForm(forms.ModelForm):
            class Meta:
                model = Ing
                fields = ('name', 'mass', 'Value', 'user')


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['brk']


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError('Bad email, bro')



