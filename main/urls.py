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
	path('قوانین_و_مقررات/',views.Ghavanin,name='ghavanin'),
	path('favorite/',views.Favorite,name='favorite_list'),
	path('gym_single/<slug>/',views.Gym_Single,name = 'gym_single'),
	path('training_class_single/<slug>/',views.Training_Single,name = 'training_single'),

	path('first_week_reservation/<slug>/', views.First_Week_Reservation, name='reservation'),
	path('second_week_reservation/<slug>/',views.Second_Week_Reservation,name = 'next_week'),
	path('third_week_reservation/<slug>/',views.Third_Week_Reservation,name = 'next_week_3'),
	path('fourth_week_reservation/<slug>/',views.Fourth_Week_Reservation,name = 'next_week_4'),

	path('accept/<slug>/', views.Accept, name='accept'),

	path('work_request/',views.Work_Request,name = 'work_request'),
	path('classes_list/',views.Classes_List,name = 'classes_list'),

	path('dashboard/',views.Dashboard,name = 'dashboard'),
	path('dashboard/delete_role_group/',views.Delete_Role_Group,name = 'delete_role_group'),
	path('dashboard/edit_profile/',views.Edit_Profile_Teacher,name = 'edit_profile'),
	path('dashboard/all_users/',views.All_Users,name = 'all_users'),
	path('dashboard/edit_gyms_info/',views.Edite_Gym_info,name='edit_gyms_info'),
	path('dashboard/add_facility/',views.Add_Facility , name = 'add_facility'),
	path('dashboard/students/',views.Students, name = 'students'),
	path('dashboard/add_province/',views.Add_province, name = 'add_province'),
	path('dashboard/add_city/',views.Add_city, name = 'add_city'),
	path('dashboard/add_area/',views.Add_area, name = 'add_area'),
	path('dashboard/add_category/',views.Add_gym_type, name = 'add_gym_type'),
	path('dashboard/teachers/',views.Teachers, name = 'teachers'),
	path('dashboard/edit_profile/<slug>/', views.Teachers_Details, name='teachers_details'),
	path('dashboard/requests/', views.Requests, name='requests'),
	path('dashboard/classes/', views.Salon_Dar_Classes, name='salon_dar_classes'),
	path('dashboard/user_classes/', views.User_Classes, name='user_classes'),
	path('dashboard/select_gym_add_class/', views.Select_Gym, name='select_gym_add_class'),
	path('dashboard/add_class/<slug>/', views.Add_Class, name='add_class'),
	path('dashboard/edit_class/<slug>/', views.Edit_class, name='edit_class'),
	path('dashboard/add_gym/', views.Add_Gym, name='add_gym'),
	path('dashboard/add_hour/<slug>/', views.Hour_Add, name='add_hour'),
	path('dashboard/select_gym_add_hour/', views.Select_Gym_add_hour, name='select_gym_add_hour'),
	path('dashboard/send_ticket/', views.Add_Ticket, name='add_ticket'),

	path('teachers/<slug>/', views.Coach_Profile, name='coach_profile'),

	re_path(r'^gyms/get/$', views.APIListGym.as_view(),name = 'apigymlist'),
	re_path(r'^hours/get/$', views.APIListHour.as_view(),name = 'apihourlist'),
	re_path(r'^tickets/get/$', views.APIListTicket.as_view(),name = 'apiticketlist'),
	re_path(r'^provinces/get-post/$', views.APIListCreateProvince.as_view(),name = 'apiprovincelist'),
	re_path(r'^cities/get-post/$', views.APIListCreateCity.as_view(),name = 'apicitylist'),
	re_path(r'^areas/get/$', views.APIListArea.as_view(),name = 'apiarealist'),
]







urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
