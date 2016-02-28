from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from django.template import loader
from django.db import IntegrityError

from .models import Question, Choice, User

class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name =  'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    def get(self, request, *args, **kwargs):
        if request.session.get('username') is None:
            return HttpResponseRedirect(reverse('poll:login'))
        return super(IndexView, self).get(request, args, kwargs)

class LoginView(generic.View):
    template_name='poll/login.html'
    def get(self, request, *args, **kwargs): #url요청이 왓을때
        template = loader.get_template('poll/login.html')
        context={}
        return HttpResponse(template.render(context,request))

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        userpw = request.POST.get("password")
        try:
            user = User.objects.get(user_name=username, user_pw=userpw)
            request.session['username'] = user.user_name
            return HttpResponseRedirect(reverse('poll:index'))
        except(User.DoesNotExist):
            return render(request, 'poll/login.html',{'error_message':"try again, wrong Id or Password ",})            

class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        request.session['username'] = None
        return HttpResponseRedirect(reverse('poll:index'))

class SignUpView(generic.View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('poll/signup.html')
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User(user_name=username, user_pw=password)
            user.save()
            return HttpResponseRedirect(reverse('poll:index'))
        except (IntegrityError):
            #return HttpResponseRedirect(reverse('poll:signup'))
            return render(request, 'poll/signup.html',{'error_message':"already exist ID",})

class DetailView(generic.DetailView):
    model=Question
    template_name = 'poll/detail.html'
    def get_queryset(self):
        """ Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        if request.session.get('username') is None:
            return HttpResponseRedirect(reverse('poll:login'))
        return super(DetailView, self).get(request, args, kwargs)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('username') is None:
            return HttpResponseRedirect(reverse('poll:login'))
        return super(ResultsView, self).get(request, args, kwargs)

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        # Redisplay the question voting form. i know what are you doing just can't understand
        return render(request, 'poll/detail.html',{'question':question,'error_message':"you didn't select a choice",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results',args=(question.id,)))

