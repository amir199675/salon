from django.conf import settings
from django.conf.urls.static import static
from django.urls import path ,re_path
from . import views
from django.urls import include

app_name = 'Main'



urlpatterns = [
	path('',views.Index,name = 'index'),

	path('gyms_list/',views.Gym_List,name='gym_list'),
	path('gyms_list/<category>/',views.Select_Category,name='select_category'),

	path('favorite/',views.Favorite,name='favorite_list'),

	path('gym_single/<slug>/',views.Gym_Single,name = 'gym_single'),

	path('first_week_reservation/<slug>/', views.First_Week_Reservation, name='reservation'),
	path('second_week_reservation/<slug>/',views.Second_Week_Reservation,name = 'next_week'),
	path('third_week_reservation/<slug>/',views.Third_Week_Reservation,name = 'next_week_3'),
	path('fourth_week_reservation/<slug>/',views.Fourth_Week_Reservation,name = 'next_week_4'),

	path('accept/<slug>/', views.Accept, name='accept'),

	path('work_request/',views.Work_Request,name = 'work_request'),
	path('classes_list/',views.Classes_List,name = 'classes_list'),

	path('dashboard/',views.Dashboard,name = 'dashboard'),
	path('dashboard/creat_gym/',views.Create_Gym , name = 'create_gym'),
	path('dashboard/delete_role_group/',views.Delete_Role_Group,name = 'delete_role_group'),
	path('dashboard/edit_profile/',views.Edit_Profile_Teacher,name = 'edit_profile'),
	path('dashboard/add_role_group/',views.Add_Role_Group,name = 'add_role_group'),
	path('dashboard/edit_gyms_info/',views.Edite_Gym_info,name='edit_gyms_info'),
	path('dashboard/add_facility/',views.Add_Facility , name = 'add_facility'),
	path('dashboard/students/',views.Students, name = 'students'),

	path('teachers/<slug>/', views.Coach_Profile, name='coach_profile'),

	re_path(r'^gyms/get/$', views.APIListGym.as_view(),name = 'apigymlist'),
	re_path(r'^hours/get/$', views.APIListHour.as_view(),name = 'apihourlist'),
	re_path(r'^tickets/get/$', views.APIListTicket.as_view(),name = 'apiticketlist'),
	re_path(r'^provinces/get-post/$', views.APIListCreateProvince.as_view(),name = 'apiprovincelist'),
	re_path(r'^cities/get-post/$', views.APIListCreateCity.as_view(),name = 'apicitylist'),
	re_path(r'^areas/get/$', views.APIListArea.as_view(),name = 'apiarealist'),
]







urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
