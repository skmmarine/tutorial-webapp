from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from django.template import loader

from .models import Question, Choice, User

class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name =  'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name = 'poll/detail.html'
    def get_queryset(self):
        """ Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'

class SignInView(generic.ListView):
    model = User
    template_name = 'poll/signin.html'

    def get_queryset(self):
        return HttpResponseRedirect(reverse('poll:index'))

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

