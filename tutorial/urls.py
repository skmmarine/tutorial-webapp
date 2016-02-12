"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^hello/', include('hello.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^another/one/', include('hello.urls'))
]
#urls라는 파일은 어떤 값이 입력되었을때 어떤 파이썬 파일을 호출해줄지 결정해주는파일.
#hello/ url이 들어오면 hello.urls 로 가서 실행을 하겟다~