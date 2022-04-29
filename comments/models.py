from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField  # markdown
from uuslug import slugify  # slug

from posts.models import Article


# Create your models here.


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    post_time = models.DateTimeField('评论时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    # 支持markdown
    comment_body = models.TextField('评论正文', max_length=300)
    # 评论者
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='评论者',
        blank=False,
        null=False,
    )
    # 评论哪篇文章
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='评论文章'
    )
    # 上级评论（comment_item_tree用），自关联
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='上级评论',
        null=True,
    )
    is_enable = models.BooleanField(
        '是否显示', default=True, null=False)

    class Meta:
        ordering = ['-post_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return str(self.author) + '评论： ' + self.comment_body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


