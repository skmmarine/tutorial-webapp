import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days) #dyas==dyas는 무슨 의미인가요??
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionViewtests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('poll:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def text_index_view_with_a_past_question(self):
        create_question(question_text="Past question.",days=-30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertContains(response, "No polls are available",status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'],[])


    def test_index_view_with_future_question_and_past_question(self):
        """미래질문 과거질문 다잇을때 과거만 나와야함!!"""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_question(self):
        #The questions index page may display multiple question
        create_question(question_text="Past question 1.",days=-30)
        create_question(question_text="Past question 2.",days=-5)
        response = self.client.get(reverse('poll:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time= timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_Question(self):
        time= timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(),False)

    def tess_was_published_recnetly_with_recent_question(self):
        time= timezone.now() - datetime.timedelta(hours=1)
        recent_question= Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(),True)

class QuestionIndexDetailtests(TestCase):

    def test_detail_view_with_a_future_question(self):
        #The detail view of a question with a pub_date in the future should
        #return a 404 not found
        future_question = create_question(question_text='Future question.',days=5)
        response = self.client.get(reverse('poll:deatail',args=(future_question.id,)))
        self.assertEqual(response.status_code,404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past questioon.',days=-5)
        response = self.client.get(reverse('poll:detail',args=(past_question.id,)))
        self.assertContains(response,past_question.question_text,status_code=200)


"""
class HelloViewTests(TestCase):
    def test_index_view_returns_message(self):
        response = self.client.get('/hello/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, Django!')
"""

