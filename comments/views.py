import logging
from django import forms
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.generic import FormView, RedirectView, ListView, DetailView, CreateView

from accounts.models import NormalUser
from posts.models import Article
from .models import Comments
from .forms import CommentsForm

import markdown
import emoji

# Create your views here.

logger = logging.getLogger(__name__)


class CommentsView(FormView):
    form_class = CommentsForm
    # 评论区渲染的页面应该是文章详情页
    template_name = 'posts/article_detail.html'

    # 定位到当前评论区的位置
    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        # 获取当前文章url（具体打开的是哪一篇文章）
        url = article.get_absolute_url()
        return self.render_to_response(self.get_form())

    # 表单数据不合法
    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        print('不合法form',form.cleaned_data)

        if self.request.user.is_authenticated:
            # 改成HiddenInput
            form.fields.update({
                'email': forms.EmailField(widget=forms.HiddenInput),
                'name': forms.CharField(widget=forms.HiddenInput),
            })
            user = self.request.user
            form.fields['email'].initial = user.email
            form.fields['name'].initial = user.username

        return self.render_to_response({
            'form': form,
            'article': article
        })

    # 表单数据合法
    def form_valid(self, form):
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        user = self.request.user
        print('合法form',form.cleaned_data)

        if not self.request.user.is_authenticated:
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            user = NormalUser.objects.get_or_create(
                username=name, email=email
            )[0]

        comment = form.save(False)
        comment.article = article
        comment.author = user
        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comments.objects.get(
                pk=form.cleaned_data['parent_comment_id']
            )
            comment.parent_comment = parent_comment
        # else:
        #     parents_comments = Comments.objects.get(pk=1)
        #     comment.parents_comments = parents_comments

        print(comment)
        comment.save(True)

        return HttpResponseRedirect(
            f'{article.get_absolute_url()}#div-comment-{comment.pk}'
        )
