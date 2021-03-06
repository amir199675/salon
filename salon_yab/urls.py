"""salon_yab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include , re_path
from .views import enamad ,SSL
from main.tasks import scheduler

app_name = 'Api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('438578.txt', enamad),
    path('',include('main.urls',namespace='Main')),
    path('Accounts/',include('Account.urls',namespace='Account')),
    re_path(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    re_path(r'^api/',include('main.urls',namespace='rest_framework')),
    path('',include('zarinpal.urls',namespace='zarinpal')),
    path('.well-known/acme-challenge/_bvZ2ittLcjrofArYcGNZr0nB0EOhbbzHdOvOUP-DpE',SSL,name='ssl'),


]

scheduler.start()
# import schedule
# import time
#
# def job():
#     print("I'm working...")
#
# schedule.every(10).seconds.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)