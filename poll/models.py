import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model): #표 하나에 열을 추가할 수 잇음
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
            #self.pub_date >= timezone.now() -datetime.timedelta(days=1)
    was_published_recently.admin_order_field='pub_date'
    was_published_recently.boolean=True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

#for login
class User(models.Model):
    user_name = models.CharField(max_length=20, unique=True)
    user_pw = models.CharField(max_length=20)

    def __str__(self):
        return self.user_name
        #return "User: " + self.user_name + ", Password: " + self.user_pw