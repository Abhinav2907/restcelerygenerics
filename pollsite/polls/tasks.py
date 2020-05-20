from celery import shared_task
from pollsite.settings import EMAIL_HOST_USER
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import send_mail
import requests
from .models import Question, Choice
from celery import task

@task(name="some_task")
def sendmail(mailid=None):
    q = Question.objects.all()
    s = ""
    for ques in q:
        nm = ques.question_text
        s = s+nm+" "
        v = Choice.objects.filter(question__question_text = nm)
        for cc in v:
            choicetext = cc.choice_text
            vott = cc.votes
            s = s+choicetext+" "+str(vott)+" "
        s = s+"/n"
    message = s
    subject = 'Info for questions'
    frommail = EMAIL_HOST_USER
    tomail = ["maanushm1@gmail.com"]
    if(mailid == None):
        pass
    else:
        tomail = tomail.append(mailid)
    send_mail(subject, message, frommail, tomail, fail_silently=False)