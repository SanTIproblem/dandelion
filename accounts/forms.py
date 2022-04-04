from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets

from . import utils
from .models import NormalUser


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "用户名", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "密码", "class": "form-control"})


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "用户名", "class": "form-control"})
        self.fields['phone_number'].widget = widgets.TextInput(
            attrs={'placeholder': "手机号（必填）", "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "邮箱（必填）", "class": "form-control"})
        self.fields['weixin_number'].widget = widgets.TextInput(
            attrs={'placeholder': "微信号（选填）", "class": "form-control"})
        self.fields['QQ_number'].widget = widgets.TextInput(
            attrs={'placeholder': "QQ号（选填）", "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "密码", "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "确认密码", "class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("该邮箱已经存在.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            raise ValidationError("该手机号已经存在.")
        return phone_number

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "phone_number", "weixin_number", "QQ_number")


class ForgetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': "密码"
            }
        ),
    )

    new_password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': "确认密码"
            }
        ),
    )

    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "邮箱"
            }
        ),
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "验证码"
            }
        ),
    )

    def clean_new_password2(self):
        password1 = self.data.get("new_password1")
        password2 = self.data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次密码不一致")
        password_validation.validate_password(password2)

        return password2

    def clean_email(self):
        user_email = self.cleaned_data.get("email")
        if not NormalUser.objects.filter(
                email=user_email
        ).exists():
            # 这里的报错提示可以判断一个邮箱是不是注册过，如果不想暴露可以修改
            raise ValidationError("未找到邮箱对应的用户")
        return user_email

    def clean_code(self):
        code = self.cleaned_data.get("code")
        error = utils.verify(
            email=self.cleaned_data.get("email"),
            code=code,
        )
        if error:
            raise ValidationError(error)
        return code


class ForgetPasswordCodeForm(forms.Form):
    email = forms.EmailField(
        label="邮箱号"
    )
