from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, ListView
from django.utils.decorators import method_decorator

from dandelion.utils import send_email, get_sha256, get_current_site, generate_code

# Create your views here.

class ArticleListView(ListView):
    template_name = 'posts/article_index.html'


class DigitalFileView(FormView):

    template_name = 'posts/digital_file.html'

    def form_valid(self, form):

        title = "提交成功！"
        content = "家访调查表已成功提交！感谢您为孩子们的付出！"
        return HttpResponseRedirect(

        )


