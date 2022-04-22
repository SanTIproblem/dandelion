import logging
from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.forms import Form
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, ListView, DetailView, CreateView
from django.utils.decorators import method_decorator

from accounts.models import NormalUser
from .models import DigitalFile, LinkShowType, Article, Category, Tag
from .forms import ArticleListForm, DigitalFileForm
from comments.forms import CommentsForm
from dandelion.utils import send_email, get_sha256, get_current_site, generate_code, cache

# Create your views here.

logger = logging.getLogger(__name__)

class ArticleListView(ListView):
    '''
    文章列表
    '''
    # ListView: 一个表示对象列表的页面。当该视图执行时，self.object_list 将包含该视图正在操作的对象列表（通常，但不一定是查询集）。

    # form_class = ArticleListForm
    template_name = 'posts/article_index.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字），此处即list
    context_object_name = 'article_list'

    # 页面类型，分类目录或标签列表等
    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'
    link_type = LinkShowType.L

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset_cache_key(self):
        """
        子类重写.获得queryset的缓存key
        """
        raise NotImplementedError()

    def get_queryset_data(self):
        """
        子类重写.获取queryset的数据
        """
        raise NotImplementedError()


    def get_queryset_from_cache(self,cache_key):
        '''
                缓存页面数据
                :param cache_key: 缓存key
                :return:
                '''
        value = cache.get(cache_key)
        # 已经存入缓存中
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        # 还没存入缓存中
        else:
            article_list = self.get_queryset_data()

            # 缓存
            cache.set(cache_key, article_list)

            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return article_list

    def get_queryset(self):
        '''
        从缓存中获取数据（ListView预置方法，此为重写）
        '''
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value

    def get_context_data(self, **kwargs):
        kwargs['linktype'] = self.link_type
        return super().get_context_data(**kwargs)


class IndexView(ArticleListView):
    '''
    首页
    '''
    link_type = LinkShowType.I

    def get_queryset_data(self):
        # 已发表的文章
        article_list = Article.objects.filter(type='a', status='p')
        return article_list

    def get_queryset_cache_key(self):
        cache_key = f'index_{self.page_number}'
        return cache_key


class ArticleDetailView(DetailView):
    '''
    文章详情
    '''

    # DetailView: 当该视图执行时，self.object 将包含该视图正在操作的对象。
    template_name = 'posts/article_detail.html'
    model = Article
    pk_url_kwarg = 'article_id'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.viewed()
        self.object = obj
        return obj

    # 返回用于显示对象的上下文数据
    def get_context_data(self, **kwargs):
        # articleid = int(self.kwargs[self.pk_url_kwarg])
        print('看看context data里都有啥：',self.object)
        comment_form = CommentsForm()
        user = self.request.user
        # 如果用户已经登录，则隐藏邮件和用户名输入框
        if user.is_authenticated and not user.is_anonymous and user.email and user.username:
            comment_form.fields.update({
                'email': forms.EmailField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            comment_form.fields["email"].initial = user.email
            comment_form.fields["name"].initial = user.username

        article_comments = self.object.comment_list()

        kwargs['form'] = comment_form
        kwargs['article_comments'] = article_comments
        kwargs['comment_count'] = len(
            article_comments) if article_comments else 0

        kwargs['next_article'] = self.object.next_article()
        kwargs['prev_article'] = self.object.prev_article()

        return super().get_context_data(**kwargs)


class EditArticleView(CreateView):
    '''
    编辑发帖
    '''

    # 牛掰，直接用django内置form把article中的属性给布置好了
    model = Article
    template_name = 'posts/edit_article.html'
    fields = ['author',
              'title',
              'content',
              # 'tags',
              ]



# 数字化档案
def get_digital_file(request):
    try:
        # 如果是POST请求，则接收表单
        if request.method == 'POST':
            # form = DigitalFileForm(request.POST)
            resp = request.POST
            print('forms:', resp)
            digi_file = DigitalFile()
            inves_name = resp['investigator']
            digi_file.investigator = NormalUser.objects.get(username=inves_name)
            digi_file.inves_time = resp['inves_time']

            # 基本信息
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
            digi_file.academic_record = resp['academic_record']
            digi_file.contact_of_teacher = resp['contact_of_teacher']
            digi_file.contact_of_parent = resp['contact_of_parent']
            digi_file.home_address = resp['home_address']
            digi_file.home_postal_code = resp['home_postal_code']
            digi_file.single_parent_or_not = resp['single_parent_or_not']
            digi_file.low_income_or_not = resp['low_income_or_not']
            digi_file.orphan_or_not = resp['orphan_or_not']
            digi_file.your_little_wish = resp['your_little_wish']
            digi_file.the_most_eager_thing_to_do = resp['the_most_eager_thing_to_do']

            # 家庭情况
            # （一对多关系：一个调查对象对多位家庭成员）


            # 家庭经济收入情况
            digi_file.debt_situation = resp['debt_situation']
            digi_file.biggest_difficulty_of_family = resp['biggest_difficulty_of_family']
            digi_file.family_assets = resp['family_assets']
            digi_file.housing_situation = resp['housing_situation']
            digi_file.main_source_of_monthly_income = resp['main_source_of_monthly_income']

            # 受资助情况
            if resp['live_in_school_or_not']:
                digi_file.live_in_school_or_not = True
            else:
                digi_file.live_in_school_or_not = False
            digi_file.expenses_of_living_in_school = resp['expenses_of_living_in_school']
            if resp['paid_or_not']:
                digi_file.paid_or_not = True
            else:
                digi_file.paid_or_not = False
            digi_file.other_help_received = resp['other_help_received']
            digi_file.reward_received = resp['reward_received']

            # 学生自述
            digi_file.statement_of_student = resp['statement_of_student']

            # 班主任评语
            digi_file.comments_of_teacher = resp['comments_of_teacher']

            # 家访手记及意见
            digi_file.home_visit_notes_and_opinions = resp['home_visit_notes_and_opinions']

            # 评定贫困程度
            if resp['orphan']:
                digi_file.orphan = True
            else:
                digi_file.orphan = False
            if resp['single_parent']:
                digi_file.single_parent = True
            else:
                digi_file.single_parent = False
            if resp['illness_or_paralysis']:
                digi_file.illness_or_paralysis = True
            else:
                digi_file.illness_or_paralysis = False
            if resp['multi_children']:
                digi_file.multi_children = True
            else:
                digi_file.multi_children = False
            if resp['lack_of_workforce']:
                digi_file.lack_of_workforce = True
            else:
                digi_file.lack_of_workforce = False
            digi_file.other_types = resp['other_types']
            digi_file.remarks = resp['remarks']

            digi_file.save()

            title = "提交成功！"
            content = "家访调查表已成功提交！感谢您为孩子们的付出！"
            return render(request, 'posts/thanks.html', {'title': title, 'content': content})

        # 如果是GET请求，则返回空表单让用户填写
        else:
            form = DigitalFileForm()
        # 没填写完则继续填写
        return render(request, 'posts/digital_file.html', {'form': form})
    except Exception as e:
        return HttpResponse('哎呀，发生错误了...', repr(e))


# 数字化档案
class DigitalFileView(FormView):
    # 要有form_class才能做后面的事
    form_class = DigitalFileForm
    template_name = 'posts/digital_file.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    def form_valid(self, form):
        print(111)
        # form = Form(data=self.request.POST)
        if form.is_valid():
            print('form: ', form)
            digi_file = form.save(False)
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


