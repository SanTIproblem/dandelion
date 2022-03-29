from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now

from dandelion.utils import get_current_site


# Create your models here.

# 普通用户
class NormalUser(AbstractUser):
    class Meta:
        ordering = ['-id']
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    nickname = models.CharField('昵称', max_length=20, blank=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    source = models.CharField("创建来源", max_length=100, blank=True)
    clean_password = models.CharField('密码', max_length=128, blank=True)

    # 逆向地址解析：https://www.cnblogs.com/kevincaptain/p/10429788.html
    def get_absolute_url(self):
        return reverse(
            'blog:author_detail', kwargs={
                'author_name': self.username})

    def __str__(self):
        return self.email

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url


# # 用户密码类
# class UserPassword(models.Model):
#     user = models.OneToOneField(
#         NormalUser,
#         on_delete=models.CASCADE,
#         verbose_name='用户',
#         related_name='普通用户'
#     )
#     clean_password = models.CharField('密码', max_length=128, blank=True)
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name = "用户密码"
#         verbose_name_plural = verbose_name
#         get_latest_by = 'id'
#
#     def __str__(self):
#         return self.user.email
