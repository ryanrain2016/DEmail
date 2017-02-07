from django.core.mail import send_mail
from django.conf import settings

from channels.generic.websockets import JsonWebsocketConsumer
from channels import Channel
from smtplib import SMTPException

import json

def sendEmail(message):
    reply_channel = message.content['reply_channel']
    content = message.content['content']
    emails = content['emails'].strip(';').split(';')
    subject = content['subject']
    from_email = content.get('from_email',settings.DEFAULT_FROM_EMAIL)
    auth_user = content.get('auth_user',settings.EMAIL_HOST_USER)
    auth_password = content.get('auth_password',settings.EMAIL_HOST_PASSWORD)
    html_message = content.get('html_message',None)
    content = content['content']
    try:
        send_mail(
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
        l = len(e.args)
        total = len(emails)
        message = '发送总数：%s;成功：%s;失败：%s'%(total,total-l,l)
        Channel(reply_channel).send({'text':json.dumps({'ret':-1,'message':message})});
        return
    Channel(reply_channel).send({'text':json.dumps({'ret':0})});


class WebConsumer(JsonWebsocketConsumer):
    http_user=True

    def connect(self, message, **kwargs): #实际应用中需要检查message.user的权限
        pass
        #如果message.user没有权限调用self.close()关闭连接

    def receive(self, content, **kwargs):
        Channel('email.send').send({
            'reply_channel':self.message.reply_channel.name,
            'content':content,
        })

    def disconnect(self, message, **kwargs):
        pass