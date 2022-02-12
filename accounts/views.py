from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.utils.decorators import method_decorator
# from django.utils.http import is_safe_url

from dandelion.utils import send_email, get_sha256, get_current_site, generate_code
from . import utils
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ForgetPasswordCodeForm
from .models import NormalUser

# Create your views here.
'''
FormView: https://www.jianshu.com/p/ac9fadf89836
函数装饰器: https://www.runoob.com/w3cnote/python-func-decorators.html
'''

# 注册
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'


    def form_valid(self, form):
        # 注册成功
        if form.is_valid():
            user = form.save(False)
            user.is_active = False
            user.source = 'Register'
            user.save(True)
            site = get_current_site().domain
            sign = get_sha256(get_sha256(settings.SECRET_KEY + str(user.id)))

            # debug
            if settings.DEBUG:
                site = '127.0.0.1:8000'
            path = reverse('account:result')
            url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(
                site=site, path=path, id=user.id, sign=sign)

            content = """
                                <p>请点击下面链接验证您的邮箱</p>

                                <a href="{url}" rel="bookmark">{url}</a>

                                再次感谢您！
                                <br />
                                如果上面链接无法打开，请将此链接复制至浏览器。
                                {url}
                                """.format(url=url)
            send_email(
                emailto=[
                    user.email,
                ],
                title='验证您的电子邮箱',
                content=content)

            url = reverse('accounts:result') + \
                  '?type=register&id=' + str(user.id)
            return HttpResponseRedirect(url)
        # 失败
        else:
            return self.render_to_response({
                'form': form
            })


# 登录
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = '/'
    login_ttl = 2626560  # 保持登录一个月

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     redirect_to = self.request.GET.get(self.redirect_field_name)
    #     if redirect_to is None:
    #         redirect_to = '/'
    #     kwargs['redirect_to'] = redirect_to
    #
    #     return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():

            # auth.login(self.request, form.get_user())
            if self.request.POST.get("remember"):
                self.request.session.set_expiry(self.login_ttl)
            return super().form_valid(form)
            # return HttpResponseRedirect('/')
        else:
            return self.render_to_response({
                'form': form
            })

    # def get_success_url(self):
    #
    #     redirect_to = self.request.POST.get(self.redirect_field_name)
    #     if not is_safe_url(
    #             url=redirect_to, allowed_hosts=[
    #                 self.request.get_host()]):
    #         redirect_to = self.success_url
    #     return redirect_to


