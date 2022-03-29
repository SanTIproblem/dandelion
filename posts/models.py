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

from dandelion.utils import cache_decorator, cache
from dandelion.utils import get_current_site

logger = logging.getLogger(__name__)


# Create your models here.

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
    pass

