from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.forms.forms import Form
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, ListView
from django.utils.decorators import method_decorator

from accounts.models import NormalUser
from .models import DigitalFile
from .forms import DigitalFileForm
from dandelion.utils import send_email, get_sha256, get_current_site, generate_code

# Create your views here.

class ArticleListView(ListView):
    template_name = 'posts/article_index.html'


# 数字化档案
def get_digital_file(request):
    # 如果是POST请求，则接收表单
    if request.method == 'POST':
        # form = DigitalFileForm(request.POST)
        resp = request.POST
        print('forms:', resp)
        digi_file = DigitalFile()
        # digi_file.name = form.cleaned_data['name']
        inves_name = resp['investigator']
        digi_file.investigator = NormalUser.objects.get(username=inves_name)
        # print(digi_file.investigator)
        digi_file.inves_time = resp['inves_time']

        digi_file.name = resp['name']
        if '男' in resp['gender']:
            digi_file.gender = 1
        elif '女' in resp['gender']:
            digi_file.gender = 0
        digi_file.birthday = resp['birthday']
        digi_file.school = resp['school']
        digi_file.grade_and_class = resp['grade_and_class']
        digi_file.school_address = resp['school_address']
        digi_file.height = resp['height']
        digi_file.weight = resp['weight']
        digi_file.shoe_size = resp['shoe_size']
        digi_file.hobbies = resp['hobbies']

        digi_file.save()

        return HttpResponseRedirect('/')

    # 如果是GET请求，则返回空表单让用户填写
    else:
        form = DigitalFileForm()
    # 没填写完则继续填写
    return render(request, 'posts/digital_file.html', {'form': form})



# 数字化档案
class DigitalFileView(FormView):
    # 要有form_class才能做后面的事
    form_class = DigitalFileForm
    template_name = 'posts/digital_file.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    def form_valid(self, form):
        print(111)
        form = Form(data=self.request.POST)
        if form.is_valid():
            print('form: ', form)
            title = "提交成功！"
            content = "家访调查表已成功提交！感谢您为孩子们的付出！"
            return HttpResponseRedirect('/login/')
        else:
            return self.render_to_response({
                'form': form
            })

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        return redirect_to


