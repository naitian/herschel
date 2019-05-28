from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def send_email(text_template, html_template, data, subject, emails, headers=None):
    text = get_template(text_template)
    html = get_template(html_template)
    text_content = text.render(data)
    html_content = html.render(data)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_FROM, emails, headers=headers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
