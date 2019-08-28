# Github.com/Rasooll
from django.conf.urls import url
from . import views

app_name = 'zarinpal'
urlpatterns = [
    url(r'^request/$', views.send_request, name='request'),
    url(r'^request_class/$', views.request_class, name='request_class'),
    url(r'^verify/$', views.verify , name='verify'),
    url(r'^verify_class/$', views.verify_class , name='verify_class'),
]
