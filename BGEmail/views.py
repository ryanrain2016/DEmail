from django.shortcuts import render
from django.http import JsonResponse

from channels import Channel
# Create your views here.

def sendEmail(request):
    if request.method=='POST':
        d = request.POST
        data = {'emails':d['emails'],'subject':d['subject'],'content':d['content']}
        Channel('email.send').send(data)
        return JsonResponse(dict(ret=0, message='提交成功'))
    return render(request,'BGEmail/bgemail.html',locals())