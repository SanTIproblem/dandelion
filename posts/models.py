import logging
from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField  # markdown
from uuslug import slugify  # slug

import accounts.models
from dandelion.utils import cache_decorator, cache
from dandelion.utils import get_current_site

logger = logging.getLogger(__name__)

# Create your models here.


'''
blank和null默认都是false
null=True表示可以为空，blank=True表示可以为空，但是不能为null
处理字符串一般不用null，一般允许空字符串
'''


# 链接类型
class LinkShowType(models.TextChoices):
    I = ('i', '首页')
    L = ('l', '列表页')
    P = ('p', '文章页面')
    A = ('a', '全站')
    S = ('s', '友情链接页面')


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        is_update_views = isinstance(
            self,
            Article) and 'update_fields' in kwargs and kwargs['update_fields'] == ['views']
        if is_update_views:
            Article.objects.filter(pk=self.pk).update(views=self.views)
        else:
            if 'slug' in self.__dict__:
                slug = getattr(
                    self, 'title') if 'title' in self.__dict__ else getattr(
                    self, 'name')
                setattr(self, 'slug', slugify(slug))
            super().save(*args, **kwargs)

    def get_full_url(self):
        site = get_current_site().domain
        url = 'https://{site}{path}'.format(site=site,
                                            path=self.get_absolute_url())
        return url

    @abstractmethod
    def get_absolute_url(self):
        pass


class Article(BaseModel):
    """文章"""

    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='作者',
        blank=False,
        null=False,
        related_name='文章'
    )
    title = models.CharField('标题', max_length=100, unique=True)
    content = models.TextField('内容', blank=False, null=False)
    published_time = models.DateTimeField('发布时间', default=now)
    views = models.PositiveIntegerField('浏览量', default=0)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    article_order = models.PositiveIntegerField('排序，值越大越前', default=0, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    category = models.ForeignKey('Category',
                                 verbose_name='文章分类',
                                 on_delete=models.CASCADE,
                                 blank=False,
                                 null=False)

    class Meta:
        ordering = ['-article_order', '-published_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


# 分类
class Category(BaseModel):
    pass


# 标签
class Tag(BaseModel):
    pass


# 数字化家访调查表
class DigitalFile(BaseModel):
    investigator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='调查人',
        blank=False,
        null=False,
    )
    inves_time = models.DateField('调查日期', default=now, blank=False, null=False)

    # 家访调查表
    # 基本信息
    # 姓名
    name = models.CharField('姓名', max_length=20, blank=False, null=False)
    # 性别
    GENDER_CHOICE = (
        (0, '女性'),
        (1, '男性')
    )
    gender = models.IntegerField('性别', choices=GENDER_CHOICE, blank=False, null=False)
    # 出生日期
    birthday = models.DateField('出生日期', blank=True)
    nation = models.CharField('民族', max_length=20, blank=True)
    school = models.CharField('在读学校', max_length=100, blank=True)
    grade_and_class = models.CharField('年级班别', max_length=50, blank=True)
    school_address = models.CharField('学校地址', max_length=100, blank=True)
    height = models.FloatField('身高', blank=True)
    weight = models.FloatField('体重', blank=True)
    shoe_size = models.FloatField('鞋码', blank=True)
    hobbies = models.CharField('特长爱好', max_length=100, blank=True)
    academic_record = models.CharField('学习成绩', max_length=200, blank=True)
    contact_of_teacher = models.CharField('班主任联系方式', max_length=100, blank=True)
    contact_of_parent = models.CharField('家长联系方式', max_length=100, blank=True)
    home_address = models.CharField('家庭住址', max_length=100, blank=True)
    home_postal_code = models.CharField('邮编', max_length=10, blank=True)
    single_parent_or_not = models.CharField('是否单亲', max_length=100, blank=True)
    low_income_or_not = models.CharField('是否低保户', max_length=100, blank=True)
    # 为记录详细情况，暂不用BooleanField
    orphan_or_not = models.CharField('是否孤儿', max_length=100, blank=True)
    your_little_wish = models.CharField('小小心愿', max_length=100, blank=True)
    the_most_eager_thing_to_do = models.CharField('最想做的事情', max_length=200, blank=True)

    # 家庭情况
    name_of_family_member = models.CharField('姓名', max_length=20, blank=True)
    relationship = models.CharField('与孩子的关系', max_length=20, blank=True)
    age = models.IntegerField('年龄', blank=True)
    occupation = models.CharField('职业', max_length=100, blank=True)
    monthly_income = models.CharField('月收入', max_length=100, blank=True)
    health_condition = models.CharField('健康状况', max_length=100, blank=True)
    basic_information = models.CharField('基本情况', max_length=200, blank=True)

    # 家庭经济收入情况
    debt_situation = models.CharField('债务情况', max_length=200, blank=True)
    biggest_difficulty_of_family = models.CharField('目前家庭最大困难', max_length=200, blank=True)
    family_assets = models.CharField('家庭资产（家用电器、主要农作物等）', max_length=200, blank=True)
    housing_situation = models.CharField('住房情况', max_length=200, blank=True)
    main_source_of_monthly_income = models.CharField('全家月收入及主要来源', max_length=200, blank=True)

    # 受资助情况
    live_in_school_or_not = models.BooleanField('是否住校', default=False, blank=True)
    expenses_of_living_in_school = models.CharField('住校费用', max_length=200, blank=True)
    paid_or_not = models.BooleanField('本学期缴费情况', default=True, blank=True)
    other_help_received = models.CharField('获得其他资助、补助、奖学金（名称及金额）', max_length=500, blank=True)
    reward_received = models.CharField('曾得到何种奖励', max_length=500, blank=True)

    # 学生自述
    statement_of_student = models.TextField('学生自述', blank=True)

    # 班主任评语
    comments_of_teacher = models.TextField('班主任评语', blank=True)

    # 家访手记及意见
    home_visit_notes_and_opinions = models.TextField('家访手记及意见', blank=True)

    # 评定贫困程度
    orphan = models.BooleanField('孤儿', default=False, blank=True)
    single_parent = models.BooleanField('单亲', default=False, blank=True)
    illness_or_paralysis = models.BooleanField('重病、残疾', default=False, blank=True)
    multi_children = models.BooleanField('多孩子读书', default=False, blank=True)
    lack_of_workforce = models.BooleanField('劳动力不足', default=False, blank=True)
    other_types = models.CharField('其他', max_length=200, blank=True)
    remarks = models.CharField('备注', max_length=200, blank=True)

    class Meta:
        ordering = ['-inves_time']
        verbose_name = '数字化家访调查表'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.name
