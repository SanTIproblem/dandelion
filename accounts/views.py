from django.contrib import auth
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
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
    # 模板文件
    form_class = RegisterForm
    template_name = 'account/registration_form.html'

    def form_valid(self, form):
        # 注册成功
        if form.is_valid():
            user = form.save(False)
            user.clean_password = form.cleaned_data['password2']
            user.is_active = False
            user.source = '注册用户'
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
    form_class = LoginForm  # 表单
    template_name = 'account/login.html'  # 渲染页面
    success_url = '/'  # 登录成功后的跳转页面
    login_ttl = 3600*24*7  # 保持登录一周
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)
        # print("form:", form)
        # print("post", self.request.POST)
        if form.is_valid():
            # 登录认证
            auth.login(self.request, form.get_user())
            if self.request.POST.get("remember"):
                self.request.session.set_expiry(self.login_ttl)
            # print('hello', self.request.user.is_authenticated)
            return super().form_valid(form)
        else:
            return self.render_to_response({
                'form': form
            })

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        # if not is_safe_url(
        #         url=redirect_to, allowed_hosts=[
        #             self.request.get_host()]):
        #     redirect_to = self.success_url
        return redirect_to


# 登出
class LogoutView(RedirectView):
    # 登出后会重定向到login界面
    url = '/login/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        # delete_sidebar_cache()
        return super().get(request, *args, **kwargs)


# Result
def account_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')

    user = get_object_or_404(get_user_model(), id=id)
    # logger.info(type)
    if user.is_active:
        return HttpResponseRedirect('/')
    if type and type in ['register', 'validation']:
        if type == 'register':
            content = '''
    恭喜您注册成功，一封验证邮件已经发送到您的邮箱：{email}，请验证您的邮箱后登录本站。
    '''.format(email=user.email)
            title = '注册成功'
        else:
            c_sign = get_sha256(get_sha256(settings.SECRET_KEY + str(user.id)))
            sign = request.GET.get('sign')
            if sign != c_sign:
                return HttpResponseForbidden()
            user.is_active = True
            user.save()
            content = '''
            恭喜您已经成功的完成邮箱验证，您现在可以使用您的账号来登录本站。
            '''
            title = '验证成功'
        return render(request, 'account/result.html', {
            'title': title,
            'content': content
        })
    else:
        return HttpResponseRedirect('/')
