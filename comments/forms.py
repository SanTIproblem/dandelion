from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.forms import Form
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import Comments
from accounts.models import NormalUser


class CommentsForm(forms.ModelForm):
    url = forms.URLField(label='网址',required=True)
    email = forms.EmailField(label='电子邮箱',required=True)
    name = forms.CharField(label='姓名',required=True)
    parent_comment_id = forms.IntegerField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comments
        fields = ['comment_body']
