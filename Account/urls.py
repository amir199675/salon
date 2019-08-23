from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'Account'


urlpatterns = [
	path('login/',views.Login,name = 'login'),
	path('logout/',views.LogOut,name = 'logout'),
	path('send_password/',views.Send_Password,name = 'send_password')
]







if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)