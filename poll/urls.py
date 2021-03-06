from django.conf.urls import url

from . import views


app_name = 'poll'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'signup/$', views.SignUpView.as_view(),name='signup'),
    url(r'login/$', views.LoginView.as_view(),name='login'),
    url(r'logout/$', views.LogoutView.as_view(),name='logout'),
    url(r'insertquestion/$', views.InsertquestionView.as_view(),name='insertquestion'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(),name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

