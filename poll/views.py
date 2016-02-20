from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from django.template import loader

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name =  'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('hello/index.html')
    context = {'latest_question_list' : latest_question_list,}
    #return HttpResponse(template.render(context, request))
    #이게 원래 형태고 그 오브젝트를 만들 때 파라미터로 tmeplate.reaner을 보내주는거
    #그러니까 랜더라는 shortcut을 만들어서 편하게 해주는거에요
    #왜냐면 return 되는건 무조건 HttpResponse 여야 하기 때문에
    return render(request, 'hello/index.html', context)
"""
class DetailView(generic.DetailView):
    model=Question
    template_name = 'poll/detail.html'
    def get_queryset(self):
        """ Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question' : question})
"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'
"""
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'hello/results.html',{'question' : question})
"""
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



"""
 이것들도 추상화의 일부다
  사용자의 입장에서는 인덱스 내부는 필요없고 그 결과만 받으면 되는거.
 """

