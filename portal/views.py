import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dandelion.settings")
django.setup()

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView


# Create your views here.

# CBV
# 门户
# class PortalView(FormView):
#     # template_name属性用于指定使用哪个模板进行渲染
#     template_name = 'portal/home.html'
#     def open_home_page(self, request):
#         response = request.GET
#         if response.status == 200:
#             return render(request, 'portal/home.html')
#         else:
#             return HttpResponse('哎呀，出错了...')

# FBV
# 首页
def open_home_page(request):
    if request.method == 'GET':
        return render(request, 'portal/home.html')
    else:
        return HttpResponse('哎呀，出错了...')