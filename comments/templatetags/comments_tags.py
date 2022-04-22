import hashlib
import logging
import random
import urllib

import bleach
from django import template
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.safestring import mark_safe

from posts.models import Article, Category, Tag, LinkShowType
from comments.models import Comments
from dandelion.utils import CommonMarkdown
from dandelion.utils import cache
from dandelion.utils import get_current_site
# from oauth.models import OAuthUser

logger = logging.getLogger(__name__)

register = template.Library()

# 评论区的tags函数


def load_comment_detail(comment, user, email):
    pass







