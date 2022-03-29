import _thread
import logging

import django.dispatch
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver


logger = logging.getLogger(__name__)

send_email_signal = django.dispatch.Signal(
    ['emailto', 'title', 'content']
)


@receiver(send_email_signal)
def send_email_signal_handler(sender, **kwargs):
    emailto = kwargs['emailto']
    title = kwargs['title']
    content = kwargs['content']

    msg = EmailMultiAlternatives(
        title,
        content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emailto)
    msg.content_subtype = "html"

    try:
        result = msg.send()
        logger.info(f'成功发送邮件：{emailto}, {result}')
    except Exception as e:
        logger.error(f"失败邮箱号: {emailto}, {e}")



