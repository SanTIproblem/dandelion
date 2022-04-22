from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.forms import Form
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import DigitalFile
from accounts.models import NormalUser

class ArticleListForm(Form):
    pass


class DigitalFileForm(forms.ModelForm):
    name = forms.CharField(label='姓名', max_length=100, required= True)
    gender = forms.CharField(label='性别', max_length=100, required=True)
    birthday = forms.DateField(label='出生日期（年/月/日）')
    # 并不会显示
    day = widgets.DateInput(
        attrs={'label':'shengri','class':'form-control'}
    )

    # 此类为ModelForm
    class Meta:
        model = DigitalFile
        fields = '__all__'







