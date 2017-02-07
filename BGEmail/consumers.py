from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException

def sendEmail(message):
    emails = message.content['emails'].strip(';').split(';')
    subject = message.content['subject']
    content = message.content['content']
    from_email = message.content.get('from_email',settings.DEFAULT_FROM_EMAIL)
    auth_user = message.content.get('auth_user',settings.EMAIL_HOST_USER)
    auth_password = message.content.get('auth_password',settings.EMAIL_HOST_PASSWORD)
    html_message = message.content.get('html_message',None)
    try:
        send_mass_mail(
            subject,
            content,
            from_email,
            emails,
            fail_silently=False,
            auth_user=auth_user,
            auth_password=auth_password,
            html_message=html_message,
        )  #auth_user,auth_password,html_message这三个参数不是必须的，这样写只是为了扩展
    except SMTPException as e:
        print(e)