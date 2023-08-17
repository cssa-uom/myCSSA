import time
from typing import Dict, List

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

from mail_owl.models import MailQuene

from .tasks import send_async_mail

# Process:
# 1. template is stringfy with the content


class AutoMailSender():
    '''
    Use for sending auto mail generated by internal apps, the template must be file based and stored in 
    'template/<app_name>/'

    '''

    def __init__(self, title: str, mail_text: str, fill_in_context: Dict[str, str], to_address: List[str], template_path: str = None) -> None:
        '''
        Init the Automail Sender
        '''

        if not title:
            raise ImproperlyConfigured(
                "AutoMail Sender must be initiated with a title")

        self.quene = MailQuene()
        self.quene.title = title
        self.quene.receiver = to_address
        self.quene.mail_text = mail_text

        # To-do: maybe need base64 support
        if template_path:
            self.quene.mail_html = render_to_string(
                template_path, fill_in_context)

    def add_to_sending_quene(self, schedule: str) -> MailQuene:
        self.quene.date_scheduled = schedule
        self.quene.save()
        return self.quene

    def send_now(self) -> MailQuene:
        start_time = time.time()
        self.quene.save()
        print("--- %s DB writing times in seconds ---" %
              (time.time() - start_time))
        send_async_mail.delay(self.quene.pk)
        return self.quene
