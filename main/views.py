from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, reverse, HttpResponse
from .models import *
from Account.models import MyUser
from django.contrib.auth import authenticate, login, user_logged_in
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import jalali_date
from datetime import date, timedelta, datetime
from django import template
from .forms import TicketForm

from django.db.models import Q

from django.contrib import sessions

from django.contrib.sessions.backends.db import SessionStore

from django.core.paginator import Paginator

from rest_framework.decorators import api_view
from rest_framework.views import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import GymsSerializer
from .serializers import HoursSerializers
from .serializers import TicketsSerializers
from .serializers import ProvincesSerializers
from .serializers import CitiesSerializers
from .serializers import AreasSerializers

from django.core.management.base import BaseCommand

from rest_framework import generics

from django.core.files.storage import FileSystemStorage


#
#
# register = template.Library()
#
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#
#         reservings = Order.objects.filter(Q(status='Reserving'))
#
#         for reserving in reservings:
#             if reserving.created + timedelta(minutes=10) < datetime.now():
#                 reserving.delete()


class APIListGym(generics.ListAPIView):
	queryset = Gym.objects.all()
	serializer_class = GymsSerializer


class APIListHour(APIView):
	def get(self, request, format=None):
		hours = Hour.objects.all()
		serializer = HoursSerializers(hours, many=True)
		return Response(serializer.data)


class APIListTicket(APIView):
	def get(self, request, format=None):
		tickets = Ticket.objects.all()
		serializer = TicketsSerializers(tickets, many=True)
		return Response(serializer.data)


class APIListCreateProvince(APIView):
	def get(self, request, format=None):
		provinces = Province.objects.all()
		serializer = ProvincesSerializers(provinces, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializers = ProvincesSerializers(data=request.data)
		serializers.is_valid(raise_exception=True)
		serializers.save()
		return Response(serializers.data, status=status.HTTP_201_CREATED)


class APIListCreateCity(APIView):
	def get(self, request, format=None):
		cites = City.objects.all()
		serializer = CitiesSerializers(cites, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializers = CitiesSerializers(data=request.data)
		id = request.data['province_id']
		province_id = Province.objects.get(id=id)
		serializers.is_valid(raise_exception=True)
		City.objects.create(name=request.data['name'], province_id=province_id)
		return Response(serializers.data, status=status.HTTP_201_CREATED)


class APIListArea(APIView):
	def get(self, request, format=None):
		areas = Area.objects.all()
		serializer = AreasSerializers(areas, many=True)
		return Response(serializer.data)


def Index(request):
	if request.method == 'POST' and 'favorite' in request.POST:
		if request.user.is_authenticated:
			user = request.user
			fav = request.POST['fav']
			try:
				favorite = Favourite.objects.get(myuser_id=MyUser.objects.get(phone_number=user),
												 gym_id=Gym.objects.get(id=fav))
				favorite.delete()
				return redirect('Main:index')
			except:
				favorite = Favourite.objects.create(myuser_id=MyUser.objects.get(phone_number=user),
													gym_id=Gym.objects.get(id=fav))
				favorite.save()
				return redirect('Main:index')

		else:
			return redirect('Accounts/login/?next=/')

	if request.user.is_authenticated:

		bascketbal = Gym.objects.filter(category_id__name='بسکتبال').count()
		footbal = Gym.objects.filter(category_id__name='فوتبال').count()
		footsal = Gym.objects.filter(category_id__name='فوتسال').count()
		volybal = Gym.objects.filter(category_id__name='والیبال').count()
		tenis = Gym.objects.filter(category_id__name='تنیس').count()
		gyms_count = Gym.objects.all().count()

		user_phone_number = request.user
		user_logged = MyUser.objects.get(phone_number=user_phone_number)
		name = user_logged.name
		user_city = user_logged.city

		favorites = Favourite.objects.filter(gym_id__area_id__city_id__name=user_city,
											 myuser_id__phone_number=user_phone_number)

		if favorites:
			pass
		else:
			favorites = {'Amir:D': 'Amir:D'}

		training_classes = Training_Class.objects.filter(gym_id__area_id__city_id__name=user_city)
		training_classes_count = training_classes.count()
		gyms = Gym.objects.filter(area_id__city_id__name=user_city).exclude(
			category_id__name='استخر')  # salon haye dar ostan user login karde
		pools = Gym.objects.filter(area_id__city_id__name=user_city, category_id__name='استخر')
		counter_comments = {}

		categories = Category.objects.all()

		# dar inja ba dictionary esm province city va area ro gereftam

		areas = Area.objects.all()
		provinces = Province.objects.all()
		cities = City.objects.all()

		for gym in gyms:
			counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

		context = {'user_logged': user_logged,
				   'gyms': gyms,
				   'name': name,
				   'counter_comments': counter_comments,
				   'training_classes_count': training_classes_count,
				   'training_classes': training_classes,
				   'areas': areas,
				   'provinces': provinces,
				   'cities': cities,
				   'categories': categories,
				   'favorites': favorites,
				   'bascketbal': bascketbal,
				   'footbal': footbal,
				   'footsal': footsal,
				   'tenis': tenis,
				   'volybal': volybal,
				   'gyms_count': gyms_count,
				   'pools': pools,
				   }
		return render(request, 'index.html', context)

	elif request.user.is_authenticated == False:

		bascketbal = Gym.objects.filter(category_id__name='بسکتبال').count()
		footbal = Gym.objects.filter(category_id__name='فوتبال').count()
		footsal = Gym.objects.filter(category_id__name='فوتسال').count()
		volybal = Gym.objects.filter(category_id__name='والیبال').count()
		tenis = Gym.objects.filter(category_id__name='تنیس').count()
		gyms_count = Gym.objects.all().count()

		counter_comments = {}

		areas = Area.objects.all()
		provinces = Province.objects.all()
		cities = City.objects.all()

		training_classes = Training_Class.objects.all()
		training_classes_count = training_classes.count()
		gyms = Gym.objects.all().exclude(category_id__name__contains='استخر')
		pools = Gym.objects.filter(category_id__name__contains='استخر')
		categories = Category.objects.all()

		for gym in gyms:
			counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

		context = {
			'training_classes': training_classes,
			'training_classes_count': training_classes_count,
			'areas': areas,
			'provinces': provinces,
			'cities': cities,
			'gyms': gyms,
			'counter_comments': counter_comments,
			'categories': categories,
			'pools': pools,
			'bascketbal': bascketbal,
			'footbal': footbal,
			'footsal': footsal,
			'tenis': tenis,
			'volybal': volybal,
			'gyms_count': gyms_count,

		}
		return render(request, 'index.html', context)


def Gym_List(request):

	if request.method == 'POST' and 'favorite' in request.POST:
		if request.user.is_authenticated:
			user = request.user
			fav = request.POST['fav']
			favorites = Favourite.objects.all()
			try:
				favorite = Favourite.objects.get(myuser_id=MyUser.objects.get(phone_number=user),
												 gym_id=Gym.objects.get(id=fav))

				favorite.delete()
				return redirect('Main:gym_list')
			except:
				favorite = Favourite.objects.create(myuser_id=MyUser.objects.get(phone_number=user),
													gym_id=Gym.objects.get(id=fav))
				favorite.save()
				return redirect('Main:gym_list')

		else:
			return redirect('Accounts/login/?next=/')

	if request.method == 'POST' and 'gym_name' in request.POST:
		name = request.POST['name']
		gyms = Gym.objects.filter(name__contains=name)
		favorites = Favourite.objects.all()

		counter_comments = {}

		selected = 'سالن های مورد نظر'

		categories = Category.objects.all()
		areas = Area.objects.all()
		provinces = Province.objects.all()
		cities = City.objects.all()

		paginator = Paginator(gyms, 10)
		page = request.GET.get('page')
		gyms_list = paginator.get_page(page)

		for gym in gyms:
			counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

		context = {
			'favorites':favorites,
			'counter_comments': counter_comments,
			'areas': areas,
			'provinces': provinces,
			'cities': cities,
			'categories': categories,
			'gyms': gyms_list,
			'selected': selected,
		}

		return render(request, 'gym_list.html', context)

	if request.method == 'GET' and 'search_gym' in request.GET:
		province = request.GET.get('province', '')
		city = request.GET.get('city', '')
		area = request.GET.get('area', '')
		category = request.GET.get('category', '')
		sex = request.GET.get('sex', '')

		gyms = Gym.objects.filter(area_id__name__contains=area, area_id__city_id__name__contains=city,
								  area_id__city_id__province_id__name__contains=province, sex__contains=sex,
								  category_id__name__contains=category)
		counter_comments = {}
		favorites = Favourite.objects.all()

		selected = 'همه سالن ها'
		if area != '':
			selected = area
		elif city != '':
			selected = city
		elif province != '':
			selected = province
		elif category != '':
			selected = category
		elif sex != '':
			selected = sex

		categories = Category.objects.all()
		areas = Area.objects.all()
		provinces = Province.objects.all()
		cities = City.objects.all()

		paginator = Paginator(gyms, 10)
		page = request.GET.get('page')
		gyms_list = paginator.get_page(page)

		for gym in gyms:
			counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

		context = {
			'favorites':favorites,
			'counter_comments': counter_comments,
			'areas': areas,
			'provinces': provinces,
			'cities': cities,
			'categories': categories,
			'gyms': gyms_list,
			'selected': selected,
		}

		return render(request, 'gym_list.html', context)



	counter_comments = {}

	categories = Category.objects.all()

	# dar inja ba dictionary esm province city va area ro gereftam

	areas = Area.objects.all()
	provinces = Province.objects.all()
	cities = City.objects.all()
	favorites = Favourite.objects.all()

	gyms = None
	if request.user.is_authenticated:
		gyms = Gym.objects.filter(area_id__city_id__name=request.user.city)
	else:
		gyms = Gym.objects.all()

	paginator = Paginator(gyms, 10)
	page = request.GET.get('page')
	gyms_list = paginator.get_page(page)

	for gym in gyms:
		counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

	selected = 'همه سالن ها'

	context = {
		'favorites':favorites,
		'counter_comments': counter_comments,
		'areas': areas,
		'provinces': provinces,
		'cities': cities,
		'categories': categories,
		'gyms': gyms_list,
		'selected': selected,

	}

	return render(request, 'gym_list.html', context)


def Select_Category(request, category):
	gyms = Gym.objects.filter(category_id__name=category)

	counter_comments = {}

	categories = Category.objects.all()

	# dar inja ba dictionary esm province city va area ro gereftam

	areas = Area.objects.all()
	provinces = Province.objects.all()
	cities = City.objects.all()

	paginator = Paginator(gyms, 10)
	page = request.GET.get('page')
	gyms_list = paginator.get_page(page)

	for gym in gyms:
		counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

	context = {

		'counter_comments': counter_comments,
		'areas': areas,
		'provinces': provinces,
		'cities': cities,
		'categories': categories,
		'gyms': gyms_list,
		'selected': category
	}

	return render(request, 'list_by_type.html', context)


def Favorite(request):
	if request.method == 'POST' and 'favorite' in request.POST:
		fav = request.POST['favo']
		user = request.user

		favorite = Favourite.objects.get(myuser_id=MyUser.objects.get(phone_number=user),
										 gym_id=Gym.objects.get(id=fav))
		favorite.delete()
		return redirect('Main:favorite_list')

	gyms = Favourite.objects.filter(myuser_id__phone_number=request.user)
	paginator = Paginator(gyms, 10)
	page = request.GET.get('page')
	gyms_list = paginator.get_page(page)

	context = {

		'gyms': gyms_list
	}

	return render(request, 'favorite.html', context)


def Gym_Single(request, slug):
	select_gym = Gym.objects.get(slug=slug)

	if request.method == 'POST' and 'favorite' in request.POST:

		if request.user.is_authenticated:
			user = request.user
			fav = request.POST['fav']
			try:
				favorite = Favourite.objects.get(myuser_id=MyUser.objects.get(phone_number=user),
												 gym_id=Gym.objects.get(id=fav))
				favorite.delete()

				return redirect('Main:gym_single', select_gym.slug)
			except:
				favorite = Favourite.objects.create(myuser_id=MyUser.objects.get(phone_number=user),
													gym_id=Gym.objects.get(id=fav))
				favorite.save()
				return redirect('Main:gym_single', select_gym.slug)


		else:
			return redirect('/Accounts/login/?next='+request.get_full_path_info())
	gyms = Gym.objects.filter(area_id__city_id__province_id__name=select_gym.area_id.city_id.province_id)

	lan = 51.65259
	lon = 32.68056

	counter_comments = {}
	for gym in gyms:
		counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

	context = {
		'lan': lan,
		'lon': lon,
		'gyms': gyms,
		'select_gym': select_gym,
		'counter_comments': counter_comments,

	}

	return render(request, 'gym_single.html', context)


def First_Week_Reservation(request, slug):
	select_gym = Gym.objects.get(slug=slug)
	hour_day_distinct = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('day')

	hours = Hour.objects.filter(Q(gym_id__slug=slug))
	hours_open = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('open')
	open = Hour.objects.filter(Q(gym_id__slug=slug))

	now = datetime.today()
	orders = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date()))

	start_week = 0
	if now.weekday() == 0:  # doshanbe
		start_week = now - timedelta(days=2)
	elif now.weekday() == 1:  # seshanbe
		start_week = now - timedelta(days=3)
	elif now.weekday() == 2:  # charshanbe
		start_week = now - timedelta(days=4)
	elif now.weekday() == 3:  # panjshanbe
		start_week = now - timedelta(days=5)
	elif now.weekday() == 4:  # jome
		start_week = now - timedelta(days=6)
	elif now.weekday() == 5:  # shanbe
		start_week = now
	elif now.weekday() == 6:  # yeshanbe
		start_week = now - timedelta(days=1)

	day_of_week = {
		"shanbe": start_week,
		"yeshanbe": start_week + timedelta(days=1), "doshanbe": start_week + timedelta(days=2),
		"seshanbe": start_week + timedelta(days=3), "charshanbe": start_week + timedelta(days=4),
		"panjshanbe": start_week + timedelta(days=5), "jome": start_week + timedelta(days=6)
	}

	orders_count = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date())).count()

	# shanbe
	shanbe = {}

	# yeshanbe
	yeshanbe = {}

	# doshanbe
	doshanbe = {}

	# seshanbe
	seshanbe = {}

	# charshanbe
	charshanbe = {}

	# panjshanbe
	panjshanbe = {}

	# jome
	jome = {}

	condition = {}

	shanbe_e = {}
	yeshanbe_e = {}
	doshanbe_e = {}
	seshanbe_e = {}
	charshanbe_e = {}
	panjshanbe_e = {}
	jome_e = {}

	for x in hours_open:
		shanbe[x.id] = True
		yeshanbe[x.id] = True
		doshanbe[x.id] = True
		seshanbe[x.id] = True
		charshanbe[x.id] = True
		panjshanbe[x.id] = True
		jome[x.id] = True
		shanbe_e[x.id] = True
		yeshanbe_e[x.id] = True
		doshanbe_e[x.id] = True
		seshanbe_e[x.id] = True
		charshanbe_e[x.id] = True
		panjshanbe_e[x.id] = True
		jome_e[x.id] = True
		for day, date in day_of_week.items():
			for hour in hours:
				if day == 'shanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						shanbe_e[x.id] = False
						shanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'shanbe' and shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									shanbe[x.id] = False

								elif order.hour_id.day == 'shanbe' and shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									shanbe[x.id] = False
				elif day == 'yeshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						yeshanbe_e[x.id] = False
						yeshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'yeshanbe' and yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									yeshanbe[x.id] = False

								elif order.hour_id.day == 'yeshanbe' and yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									yeshanbe[x.id] = False

				elif day == 'doshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						doshanbe_e[x.id] = False
						doshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:

								if order.hour_id.day == 'doshanbe' and doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									doshanbe[x.id] = False

								elif order.hour_id.day == 'doshanbe' and doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									doshanbe[x.id] = False

				elif day == 'seshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						seshanbe_e[x.id] = False
						seshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'seshanbe' and seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									seshanbe[x.id] = False

								elif order.hour_id.day == 'seshanbe' and seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									seshanbe[x.id] = False

				elif day == 'charshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						charshanbe_e[x.id] = False
						charshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'charshanbe' and charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									charshanbe[x.id] = False

								elif order.hour_id.day == 'charshanbe' and charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									charshanbe[x.id] = False

				elif day == 'panjshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						panjshanbe_e[x.id] = False
						panjshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'panjshanbe' and panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									panjshanbe[x.id] = False

								elif order.hour_id.day == 'panjshanbe' and panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									panjshanbe[x.id] = False

				elif day == 'jome':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						jome_e[x.id] = False
						jome[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'jome' and jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									jome[x.id] = False

								elif order.hour_id.day == 'jome' and jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									jome[x.id] = False

	shanbe_t = {}
	for x in hours_open:
		shanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in shanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'shanbe' and hour.open == x.open or key == hour.id and hour.day == 'shanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						shanbe_t[x.id] = False

	yeshanbe_t = {}
	for x in hours_open:
		yeshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in yeshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'yeshanbe' and hour.open == x.open or key == hour.id and hour.day == 'yeshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						yeshanbe_t[x.id] = False

	doshanbe_t = {}
	for x in hours_open:
		doshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in doshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'doshanbe' and hour.open == x.open or key == hour.id and hour.day == 'doshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						doshanbe_t[x.id] = False

	seshanbe_t = {}
	for x in hours_open:
		seshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in seshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'seshanbe' and hour.open == x.open or key == hour.id and hour.day == 'seshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						seshanbe_t[x.id] = False

	charshanbe_t = {}
	for x in hours_open:
		charshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in charshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'charshanbe' and hour.open == x.open or key == hour.id and hour.day == 'charshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						charshanbe_t[x.id] = False

	panjshanbe_t = {}
	for x in hours_open:
		panjshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in panjshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'panjshanbe' and hour.open == x.open or key == hour.id and hour.day == 'panjshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						panjshanbe_t[x.id] = False

	jome_t = {}
	for x in hours_open:
		jome_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in jome.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'jome' and hour.open == x.open or key == hour.id and hour.day == 'jome' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						jome_t[x.id] = False

	next_key = True
	back_key = False
	first_week = True

	context = {
		'next_key': next_key,
		'back_key': back_key,
		'first_week': first_week,
		'day_of_week': day_of_week,
		'now': now,
		'select_gym': select_gym,
		'hours_open': hours_open,
		'hours': hours,
		'orders_count': orders_count,
		'orders': orders,
		'shanbe_e': shanbe_e,
		'shanbe': shanbe,
		'shanbe_t': shanbe_t,
		'yeshanbe_e': yeshanbe_e,
		'yeshanbe': yeshanbe,
		'yeshanbe_t': yeshanbe_t,
		'doshanbe_e': doshanbe_e,
		'doshanbe': doshanbe,
		'doshanbe_t': doshanbe_t,
		'seshanbe_e': seshanbe_e,
		'seshanbe': seshanbe,
		'seshanbe_t': seshanbe_t,
		'charshanbe_e': charshanbe_e,
		'charshanbe': charshanbe,
		'charshanbe_t': charshanbe_t,
		'panjshanbe_e': panjshanbe_e,
		'panjshanbe': panjshanbe,
		'panjshanbe_t': panjshanbe_t,
		'jome_e': jome_e,
		'jome': jome,
		'jome_t': jome_t,
		'start_week': start_week,

	}
	return render(request, 'reserve_thisweek.html', context)


def Second_Week_Reservation(request, slug):
	select_gym = Gym.objects.get(slug=slug)
	hour_day_distinct = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('day')

	hours = Hour.objects.filter(Q(gym_id__slug=slug))
	hours_open = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('open')
	open = Hour.objects.filter(Q(gym_id__slug=slug))

	now = datetime.today()
	orders = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date()))
	orders_count = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date())).count()

	start_week = now + timedelta(weeks=1)
	if now.weekday() == 0:  # shanbe
		start_week = start_week - timedelta(days=2)
	elif now.weekday() == 1:  # yekshanbe
		start_week = start_week - timedelta(days=3)
	elif now.weekday() == 2:  # doahanbe
		start_week = start_week - timedelta(days=4)
	elif now.weekday() == 3:  # seshanbe
		start_week = start_week - timedelta(days=5)
	elif now.weekday() == 4:  # charshanbe
		start_week = start_week - timedelta(days=6)
	elif now.weekday() == 5:  # panjshanbe
		start_week = start_week
	elif now.weekday() == 6:  # jome
		start_week = start_week - timedelta(days=1)

	day_of_week = {"shanbe": start_week,
				   "yeshanbe": start_week + timedelta(days=1), "doshanbe": start_week + timedelta(days=2),
				   "seshanbe": start_week + timedelta(days=3), "charshanbe": start_week + timedelta(days=4),
				   "panjshanbe": start_week + timedelta(days=5), "jome": start_week + timedelta(days=6)
				   }

	# shanbe
	shanbe = {}
	#
	# yeshanbe
	yeshanbe = {}

	# doshanbe
	doshanbe = {}

	# seshanbe
	seshanbe = {}

	# charshanbe
	charshanbe = {}

	# panjshanbe
	panjshanbe = {}

	# jome
	jome = {}

	condition = {}

	shanbe_e = {}
	yeshanbe_e = {}
	doshanbe_e = {}
	seshanbe_e = {}
	charshanbe_e = {}
	panjshanbe_e = {}
	jome_e = {}

	for x in hours_open:
		shanbe[x.id] = True
		yeshanbe[x.id] = True
		doshanbe[x.id] = True
		seshanbe[x.id] = True
		charshanbe[x.id] = True
		panjshanbe[x.id] = True
		jome[x.id] = True
		shanbe_e[x.id] = True
		yeshanbe_e[x.id] = True
		doshanbe_e[x.id] = True
		seshanbe_e[x.id] = True
		charshanbe_e[x.id] = True
		panjshanbe_e[x.id] = True
		jome_e[x.id] = True
		for day, date in day_of_week.items():
			for hour in hours:
				if day == 'shanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						shanbe_e[x.id] = False
						shanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									shanbe[x.id] = False

								elif shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									shanbe[x.id] = False
				elif day == 'yeshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						yeshanbe_e[x.id] = False
						yeshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									yeshanbe[x.id] = False

								elif yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									yeshanbe[x.id] = False

				elif day == 'doshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						doshanbe_e[x.id] = False
						doshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									doshanbe[x.id] = False

								elif doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									doshanbe[x.id] = False

				elif day == 'seshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						seshanbe_e[x.id] = False
						seshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									seshanbe[x.id] = False

								elif seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									seshanbe[x.id] = False

				elif day == 'charshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						charshanbe_e[x.id] = False
						charshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									charshanbe[x.id] = False

								elif charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									charshanbe[x.id] = False

				elif day == 'panjshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						panjshanbe_e[x.id] = False
						panjshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									panjshanbe[x.id] = False

								elif panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									panjshanbe[x.id] = False

				elif day == 'jome':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						jome_e[x.id] = False
						jome[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									jome[x.id] = False

								elif jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									jome[x.id] = False

	shanbe_t = {}
	for x in hours_open:
		shanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in shanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'shanbe' and hour.open == x.open or key == hour.id and hour.day == 'shanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						shanbe_t[x.id] = False

	yeshanbe_t = {}
	for x in hours_open:
		yeshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in yeshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'yeshanbe' and hour.open == x.open or key == hour.id and hour.day == 'yeshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						yeshanbe_t[x.id] = False

	doshanbe_t = {}
	for x in hours_open:
		doshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in doshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'doshanbe' and hour.open == x.open or key == hour.id and hour.day == 'doshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						doshanbe_t[x.id] = False

	seshanbe_t = {}
	for x in hours_open:
		seshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in seshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'seshanbe' and hour.open == x.open or key == hour.id and hour.day == 'seshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						seshanbe_t[x.id] = False

	charshanbe_t = {}
	for x in hours_open:
		charshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in charshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'charshanbe' and hour.open == x.open or key == hour.id and hour.day == 'charshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						charshanbe_t[x.id] = False

	panjshanbe_t = {}
	for x in hours_open:
		panjshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in panjshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'panjshanbe' and hour.open == x.open or key == hour.id and hour.day == 'panjshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						panjshanbe_t[x.id] = False

	jome_t = {}
	for x in hours_open:
		jome_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in jome.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'jome' and hour.open == x.open or key == hour.id and hour.day == 'jome' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						jome_t[x.id] = False

	next_key = True
	back_key = True
	second_week = True

	context = {
		'next_key': next_key,
		'back_key': back_key,
		'second_week': second_week,
		'day_of_week': day_of_week,
		'now': now,
		'select_gym': select_gym,
		'start_week': start_week,
		'hours_open': hours_open,
		'hours': hours,
		'orders_count': orders_count,
		'orders': orders,
		'shanbe_e': shanbe_e,
		'shanbe': shanbe,
		'shanbe_t': shanbe_t,
		'yeshanbe_e': yeshanbe_e,
		'yeshanbe': yeshanbe,
		'yeshanbe_t': yeshanbe_t,
		'doshanbe_e': doshanbe_e,
		'doshanbe': doshanbe,
		'doshanbe_t': doshanbe_t,
		'seshanbe_e': seshanbe_e,
		'seshanbe': seshanbe,
		'seshanbe_t': seshanbe_t,
		'charshanbe_e': charshanbe_e,
		'charshanbe': charshanbe,
		'charshanbe_t': charshanbe_t,
		'panjshanbe_e': panjshanbe_e,
		'panjshanbe': panjshanbe,
		'panjshanbe_t': panjshanbe_t,
		'jome_e': jome_e,
		'jome': jome,
		'jome_t': jome_t,

	}
	return render(request, 'reserve_thisweek.html', context)


def Third_Week_Reservation(request, slug):
	select_gym = Gym.objects.get(slug=slug)
	hour_day_distinct = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('day')

	hours = Hour.objects.filter(Q(gym_id__slug=slug))
	hours_open = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('open')
	open = Hour.objects.filter(Q(gym_id__slug=slug))

	now = datetime.today()
	orders = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date()))

	start_week = now + timedelta(weeks=2)
	if now.weekday() == 0:  # shanbe
		start_week = start_week - timedelta(days=2)
	elif now.weekday() == 1:  # yekshanbe
		start_week = start_week - timedelta(days=3)
	elif now.weekday() == 2:  # doahanbe
		start_week = start_week - timedelta(days=4)
	elif now.weekday() == 3:  # seshanbe
		start_week = start_week - timedelta(days=5)
	elif now.weekday() == 4:  # charshanbe
		start_week = start_week - timedelta(days=6)
	elif now.weekday() == 5:  # panjshanbe
		start_week = start_week
	elif now.weekday() == 6:  # jome
		start_week = start_week - timedelta(days=1)

	day_of_week = {"shanbe": start_week,
				   "yeshanbe": start_week + timedelta(days=1), "doshanbe": start_week + timedelta(days=2),
				   "seshanbe": start_week + timedelta(days=3), "charshanbe": start_week + timedelta(days=4),
				   "panjshanbe": start_week + timedelta(days=5), "jome": start_week + timedelta(days=6)
				   }

	orders_count = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date())).count()

	# shanbe
	shanbe = {}

	# yeshanbe
	yeshanbe = {}

	# doshanbe
	doshanbe = {}

	# seshanbe
	seshanbe = {}

	# charshanbe
	charshanbe = {}

	# panjshanbe
	panjshanbe = {}

	# jome
	jome = {}

	condition = {}

	shanbe_e = {}
	yeshanbe_e = {}
	doshanbe_e = {}
	seshanbe_e = {}
	charshanbe_e = {}
	panjshanbe_e = {}
	jome_e = {}

	for x in hours_open:
		shanbe[x.id] = True
		yeshanbe[x.id] = True
		doshanbe[x.id] = True
		seshanbe[x.id] = True
		charshanbe[x.id] = True
		panjshanbe[x.id] = True
		jome[x.id] = True
		shanbe_e[x.id] = True
		yeshanbe_e[x.id] = True
		doshanbe_e[x.id] = True
		seshanbe_e[x.id] = True
		charshanbe_e[x.id] = True
		panjshanbe_e[x.id] = True
		jome_e[x.id] = True
		for day, date in day_of_week.items():
			for hour in hours:
				if day == 'shanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						shanbe_e[x.id] = False
						shanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									shanbe[x.id] = False

								elif shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									shanbe[x.id] = False
				elif day == 'yeshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						yeshanbe_e[x.id] = False
						yeshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									yeshanbe[x.id] = False

								elif yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									yeshanbe[x.id] = False

				elif day == 'doshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						doshanbe_e[x.id] = False
						doshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									doshanbe[x.id] = False

								elif doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									doshanbe[x.id] = False

				elif day == 'seshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						seshanbe_e[x.id] = False
						seshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									seshanbe[x.id] = False

								elif seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									seshanbe[x.id] = False

				elif day == 'charshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						charshanbe_e[x.id] = False
						charshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									charshanbe[x.id] = False

								elif charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									charshanbe[x.id] = False

				elif day == 'panjshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						panjshanbe_e[x.id] = False
						panjshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									panjshanbe[x.id] = False

								elif panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									panjshanbe[x.id] = False

				elif day == 'jome':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						jome_e[x.id] = False
						jome[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									jome[x.id] = False

								elif jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									jome[x.id] = False

	shanbe_t = {}
	for x in hours_open:
		shanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in shanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'shanbe' and hour.open == x.open or key == hour.id and hour.day == 'shanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						shanbe_t[x.id] = False

	yeshanbe_t = {}
	for x in hours_open:
		yeshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in yeshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'yeshanbe' and hour.open == x.open or key == hour.id and hour.day == 'yeshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						yeshanbe_t[x.id] = False

	doshanbe_t = {}
	for x in hours_open:
		doshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in doshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'doshanbe' and hour.open == x.open or key == hour.id and hour.day == 'doshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						doshanbe_t[x.id] = False

	seshanbe_t = {}
	for x in hours_open:
		seshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in seshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'seshanbe' and hour.open == x.open or key == hour.id and hour.day == 'seshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						seshanbe_t[x.id] = False

	charshanbe_t = {}
	for x in hours_open:
		charshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in charshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'charshanbe' and hour.open == x.open or key == hour.id and hour.day == 'charshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						charshanbe_t[x.id] = False

	panjshanbe_t = {}
	for x in hours_open:
		panjshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in panjshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'panjshanbe' and hour.open == x.open or key == hour.id and hour.day == 'panjshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						panjshanbe_t[x.id] = False

	jome_t = {}
	for x in hours_open:
		jome_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in jome.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'jome' and hour.open == x.open or key == hour.id and hour.day == 'jome' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						jome_t[x.id] = False

	next_key = True
	back_key = True
	third_week = True

	context = {
		'next_key': next_key,
		'back_key': back_key,
		'third_week': third_week,
		'day_of_week': day_of_week,
		'now': now,
		'select_gym': select_gym,
		'hours_open': hours_open,
		'hours': hours,
		'orders_count': orders_count,
		'orders': orders,
		'shanbe_e': shanbe_e,
		'shanbe': shanbe,
		'shanbe_t': shanbe_t,
		'yeshanbe_e': yeshanbe_e,
		'yeshanbe': yeshanbe,
		'yeshanbe_t': yeshanbe_t,
		'doshanbe_e': doshanbe_e,
		'doshanbe': doshanbe,
		'doshanbe_t': doshanbe_t,
		'seshanbe_e': seshanbe_e,
		'seshanbe': seshanbe,
		'seshanbe_t': seshanbe_t,
		'charshanbe_e': charshanbe_e,
		'charshanbe': charshanbe,
		'charshanbe_t': charshanbe_t,
		'panjshanbe_e': panjshanbe_e,
		'panjshanbe': panjshanbe,
		'panjshanbe_t': panjshanbe_t,
		'jome_e': jome_e,
		'jome': jome,
		'jome_t': jome_t,

	}

	return render(request, 'reserve_thisweek.html', context)


def Fourth_Week_Reservation(request, slug):
	select_gym = Gym.objects.get(slug=slug)
	hour_day_distinct = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('day')

	hours = Hour.objects.filter(Q(gym_id__slug=slug))
	hours_open = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('open')
	open = Hour.objects.filter(Q(gym_id__slug=slug))

	now = datetime.today()
	orders = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date()))

	start_week = now + timedelta(weeks=3)
	if now.weekday() == 0:  # shanbe
		start_week = start_week - timedelta(days=2)
	elif now.weekday() == 1:  # yekshanbe
		start_week = start_week - timedelta(days=3)
	elif now.weekday() == 2:  # doahanbe
		start_week = start_week - timedelta(days=4)
	elif now.weekday() == 3:  # seshanbe
		start_week = start_week - timedelta(days=5)
	elif now.weekday() == 4:  # charshanbe
		start_week = start_week - timedelta(days=6)
	elif now.weekday() == 5:  # panjshanbe
		start_week = start_week
	elif now.weekday() == 6:  # jome
		start_week = start_week - timedelta(days=1)

	day_of_week = {"shanbe": start_week,
				   "yeshanbe": start_week + timedelta(days=1), "doshanbe": start_week + timedelta(days=2),
				   "seshanbe": start_week + timedelta(days=3), "charshanbe": start_week + timedelta(days=4),
				   "panjshanbe": start_week + timedelta(days=5), "jome": start_week + timedelta(days=6)
				   }

	orders_count = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date())).count()

	# shanbe
	shanbe = {}

	# yeshanbe
	yeshanbe = {}

	# doshanbe
	doshanbe = {}

	# seshanbe
	seshanbe = {}

	# charshanbe
	charshanbe = {}

	# panjshanbe
	panjshanbe = {}

	# jome
	jome = {}

	condition = {}

	shanbe_e = {}
	yeshanbe_e = {}
	doshanbe_e = {}
	seshanbe_e = {}
	charshanbe_e = {}
	panjshanbe_e = {}
	jome_e = {}

	for x in hours_open:
		shanbe[x.id] = True
		yeshanbe[x.id] = True
		doshanbe[x.id] = True
		seshanbe[x.id] = True
		charshanbe[x.id] = True
		panjshanbe[x.id] = True
		jome[x.id] = True
		shanbe_e[x.id] = True
		yeshanbe_e[x.id] = True
		doshanbe_e[x.id] = True
		seshanbe_e[x.id] = True
		charshanbe_e[x.id] = True
		panjshanbe_e[x.id] = True
		jome_e[x.id] = True
		for day, date in day_of_week.items():
			for hour in hours:
				if day == 'shanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						shanbe_e[x.id] = False
						shanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'shanbe' and shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									shanbe[x.id] = False

								elif order.hour_id.day == 'shanbe' and shanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									shanbe[x.id] = False
				elif day == 'yeshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						yeshanbe_e[x.id] = False
						yeshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'yeshanbe' and yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									yeshanbe[x.id] = False

								elif order.hour_id.day == 'yeshanbe' and yeshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									yeshanbe[x.id] = False

				elif day == 'doshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						doshanbe_e[x.id] = False
						doshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:

								if order.hour_id.day == 'doshanbe' and doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									doshanbe[x.id] = False

								elif order.hour_id.day == 'doshanbe' and doshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									doshanbe[x.id] = False

				elif day == 'seshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						seshanbe_e[x.id] = False
						seshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'seshanbe' and seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									seshanbe[x.id] = False

								elif order.hour_id.day == 'seshanbe' and seshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									seshanbe[x.id] = False

				elif day == 'charshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						charshanbe_e[x.id] = False
						charshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'charshanbe' and charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									charshanbe[x.id] = False

								elif order.hour_id.day == 'charshanbe' and charshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									charshanbe[x.id] = False

				elif day == 'panjshanbe':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						panjshanbe_e[x.id] = False
						panjshanbe[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'panjshanbe' and panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									panjshanbe[x.id] = False

								elif order.hour_id.day == 'panjshanbe' and panjshanbe_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									panjshanbe[x.id] = False

				elif day == 'jome':
					if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
						jome_e[x.id] = False
						jome[x.id] = False
					for hour in hours:
						if orders_count:
							for order in orders:
								if order.hour_id.day == 'jome' and jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
									jome[x.id] = False

								elif order.hour_id.day == 'jome' and jome_e[
									x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
									jome[x.id] = False

	shanbe_t = {}
	for x in hours_open:
		shanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in shanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'shanbe' and hour.open == x.open or key == hour.id and hour.day == 'shanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						shanbe_t[x.id] = False

	yeshanbe_t = {}
	for x in hours_open:
		yeshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in yeshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'yeshanbe' and hour.open == x.open or key == hour.id and hour.day == 'yeshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						yeshanbe_t[x.id] = False

	doshanbe_t = {}
	for x in hours_open:
		doshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in doshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'doshanbe' and hour.open == x.open or key == hour.id and hour.day == 'doshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						doshanbe_t[x.id] = False

	seshanbe_t = {}
	for x in hours_open:
		seshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in seshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'seshanbe' and hour.open == x.open or key == hour.id and hour.day == 'seshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						seshanbe_t[x.id] = False

	charshanbe_t = {}
	for x in hours_open:
		charshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in charshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'charshanbe' and hour.open == x.open or key == hour.id and hour.day == 'charshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						charshanbe_t[x.id] = False

	panjshanbe_t = {}
	for x in hours_open:
		panjshanbe_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in panjshanbe.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'panjshanbe' and hour.open == x.open or key == hour.id and hour.day == 'panjshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						panjshanbe_t[x.id] = False

	jome_t = {}
	for x in hours_open:
		jome_t[x.id] = True
		for day, date in day_of_week.items():

			for hour in hours:
				for key, value in jome.items():
					if key == x.id and value == True and date.date() > now.date() and hour.day == 'jome' and hour.open == x.open or key == hour.id and hour.day == 'jome' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
						jome_t[x.id] = False

	next_key = False
	back_key = True
	fourth_week = True

	context = {
		'next_key': next_key,
		'back_key': back_key,
		'fourth_week': fourth_week,
		'day_of_week': day_of_week,
		'now': now,
		'select_gym': select_gym,
		'hours_open': hours_open,
		'hours': hours,
		'orders_count': orders_count,
		'orders': orders,
		'shanbe_e': shanbe_e,
		'shanbe': shanbe,
		'shanbe_t': shanbe_t,
		'yeshanbe_e': yeshanbe_e,
		'yeshanbe': yeshanbe,
		'yeshanbe_t': yeshanbe_t,
		'doshanbe_e': doshanbe_e,
		'doshanbe': doshanbe,
		'doshanbe_t': doshanbe_t,
		'seshanbe_e': seshanbe_e,
		'seshanbe': seshanbe,
		'seshanbe_t': seshanbe_t,
		'charshanbe_e': charshanbe_e,
		'charshanbe': charshanbe,
		'charshanbe_t': charshanbe_t,
		'panjshanbe_e': panjshanbe_e,
		'panjshanbe': panjshanbe,
		'panjshanbe_t': panjshanbe_t,
		'jome_e': jome_e,
		'jome': jome,
		'jome_t': jome_t,

	}

	return render(request, 'reserve_thisweek.html', context)


def Accept(request, slug):
	if request.method == 'POST' and 'description' in request.POST:
		s_day = request.POST['day']
		s_status = request.POST['status']
		s_description = request.POST['description']
		s_myuser_id = request.POST['myuser']
		s_gym_id = request.POST['gymid']
		s_hour_id = request.POST['hourid']
		s_order_date = request.POST['date']
		s_total_price = request.POST['totalprice']
		s_paid_money = request.POST['paidmoney']
		s_order_date = s_order_date.replace(',', '')
		s_order_date = s_order_date.replace('.', '')
		if 'Sept' in s_order_date:
			s_order_date = s_order_date.replace('t', '')

		try:
			order_date = datetime.strptime(s_order_date, '%B %d %Y')
		except:
			order_date = datetime.strptime(s_order_date, '%b %d %Y')
		# order = Order.objects.create(order_date=order_date,
		#                              gym_id=Gym.objects.get(id=s_gym_id),
		#                              myuser_id=MyUser.objects.get(phone_number=request.user),
		#                              hour_id=Hour.objects.get(id=s_hour_id),
		#                              total_price=s_total_price,
		#                              paid_money=s_paid_money,
		#                              status='Reserving')

		select_gym = Gym.objects.get(slug=slug)

		hour_day_distinct = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('day')

		hours = Hour.objects.filter(Q(gym_id__slug=slug))
		hours_open = Hour.objects.filter(Q(gym_id__slug=slug)).distinct('open')
		open = Hour.objects.filter(Q(gym_id__slug=slug))

		now = datetime.today()
		orders = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date()))

		start_week = 0
		if now.weekday() == 0:  # doshanbe
			start_week = now - timedelta(days=2)
		elif now.weekday() == 1:  # seshanbe
			start_week = now - timedelta(days=3)
		elif now.weekday() == 2:  # charshanbe
			start_week = now - timedelta(days=4)
		elif now.weekday() == 3:  # panjshanbe
			start_week = now - timedelta(days=5)
		elif now.weekday() == 4:  # jome
			start_week = now - timedelta(days=6)
		elif now.weekday() == 5:  # shanbe
			start_week = now
		elif now.weekday() == 6:  # yeshanbe
			start_week = now - timedelta(days=1)

		day_of_week = {
			"shanbe": start_week,
			"yeshanbe": start_week + timedelta(days=1), "doshanbe": start_week + timedelta(days=2),
			"seshanbe": start_week + timedelta(days=3), "charshanbe": start_week + timedelta(days=4),
			"panjshanbe": start_week + timedelta(days=5), "jome": start_week + timedelta(days=6)
		}

		orders_count = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date())).count()

		# shanbe
		shanbe = {}

		# yeshanbe
		yeshanbe = {}

		# doshanbe
		doshanbe = {}

		# seshanbe
		seshanbe = {}

		# charshanbe
		charshanbe = {}

		# panjshanbe
		panjshanbe = {}

		# jome
		jome = {}

		condition = {}

		shanbe_e = {}
		yeshanbe_e = {}
		doshanbe_e = {}
		seshanbe_e = {}
		charshanbe_e = {}
		panjshanbe_e = {}
		jome_e = {}

		for x in hours_open:
			shanbe[x.id] = True
			yeshanbe[x.id] = True
			doshanbe[x.id] = True
			seshanbe[x.id] = True
			charshanbe[x.id] = True
			panjshanbe[x.id] = True
			jome[x.id] = True
			shanbe_e[x.id] = True
			yeshanbe_e[x.id] = True
			doshanbe_e[x.id] = True
			seshanbe_e[x.id] = True
			charshanbe_e[x.id] = True
			panjshanbe_e[x.id] = True
			jome_e[x.id] = True
			for day, date in day_of_week.items():
				for hour in hours:
					if day == 'shanbe':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							shanbe_e[x.id] = False
							shanbe[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:
									if order.hour_id.day == 'shanbe' and shanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										shanbe[x.id] = False

									elif order.hour_id.day == 'shanbe' and shanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										shanbe[x.id] = False
					elif day == 'yeshanbe':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							yeshanbe_e[x.id] = False
							yeshanbe[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:
									if order.hour_id.day == 'yeshanbe' and yeshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										yeshanbe[x.id] = False

									elif order.hour_id.day == 'yeshanbe' and yeshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										yeshanbe[x.id] = False

					elif day == 'doshanbe':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							doshanbe_e[x.id] = False
							doshanbe[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:

									if order.hour_id.day == 'doshanbe' and doshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										doshanbe[x.id] = False

									elif order.hour_id.day == 'doshanbe' and doshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										doshanbe[x.id] = False

					elif day == 'seshanbe':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							seshanbe_e[x.id] = False
							seshanbe[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:
									if order.hour_id.day == 'seshanbe' and seshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										seshanbe[x.id] = False

									elif order.hour_id.day == 'seshanbe' and seshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										seshanbe[x.id] = False

					elif day == 'charshanbe':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							charshanbe_e[x.id] = False
							charshanbe[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:
									if order.hour_id.day == 'charshanbe' and charshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										charshanbe[x.id] = False

									elif order.hour_id.day == 'charshanbe' and charshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										charshanbe[x.id] = False

					elif day == 'panjshanbe':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							panjshanbe_e[x.id] = False
							panjshanbe[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:
									if order.hour_id.day == 'panjshanbe' and panjshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										panjshanbe[x.id] = False

									elif order.hour_id.day == 'panjshanbe' and panjshanbe_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										panjshanbe[x.id] = False

					elif day == 'jome':
						if date.date() < now.date() or date.date() == now.date() and x.open < now.time():
							jome_e[x.id] = False
							jome[x.id] = False
						for hour in hours:
							if orders_count:
								for order in orders:
									if order.hour_id.day == 'jome' and jome_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserved':
										jome[x.id] = False

									elif order.hour_id.day == 'jome' and jome_e[
										x.id] and order.order_date == date.date() and order.hour_id.day == hour.day and order.hour_id.open == x.open and x.open == hour.open and order.hour_id.open == hour.open and order.status == 'Reserving':
										jome[x.id] = False

		shanbe_t = {}
		for x in hours_open:
			shanbe_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in shanbe.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'shanbe' and hour.open == x.open or key == hour.id and hour.day == 'shanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							shanbe_t[x.id] = False

		yeshanbe_t = {}
		for x in hours_open:
			yeshanbe_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in yeshanbe.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'yeshanbe' and hour.open == x.open or key == hour.id and hour.day == 'yeshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							yeshanbe_t[x.id] = False

		doshanbe_t = {}
		for x in hours_open:
			doshanbe_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in doshanbe.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'doshanbe' and hour.open == x.open or key == hour.id and hour.day == 'doshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							doshanbe_t[x.id] = False

		seshanbe_t = {}
		for x in hours_open:
			seshanbe_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in seshanbe.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'seshanbe' and hour.open == x.open or key == hour.id and hour.day == 'seshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							seshanbe_t[x.id] = False

		charshanbe_t = {}
		for x in hours_open:
			charshanbe_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in charshanbe.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'charshanbe' and hour.open == x.open or key == hour.id and hour.day == 'charshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							charshanbe_t[x.id] = False

		panjshanbe_t = {}
		for x in hours_open:
			panjshanbe_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in panjshanbe.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'panjshanbe' and hour.open == x.open or key == hour.id and hour.day == 'panjshanbe' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							panjshanbe_t[x.id] = False

		jome_t = {}
		for x in hours_open:
			jome_t[x.id] = True
			for day, date in day_of_week.items():

				for hour in hours:
					for key, value in jome.items():
						if key == x.id and value == True and date.date() > now.date() and hour.day == 'jome' and hour.open == x.open or key == hour.id and hour.day == 'jome' and value == True and date.date() == now.date() and hour.open > now.time() and hour.open == x.open:
							jome_t[x.id] = False

		next_key = True
		back_key = False
		user_phone_number = request.user

		user_logged = MyUser.objects.get(phone_number=user_phone_number)
		roles_user = None
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		for rol in roles_user:
			if rol.name == 'superuser':

				order = Order.objects.create(order_date=order_date,
											 gym_id=select_gym,
											 myuser_id=user_logged,
											 hour_id=Hour.objects.get(id=s_hour_id),
											 total_price=s_total_price,
											 paid_money=s_paid_money,
											 status='Reserved',
											 description='رزرو شده توسظ سوپر یوزر')
				return redirect('Main:reservation', select_gym.slug)

			elif rol.name == 'مسئول منطقه' and request.user.city == select_gym.area_id.city_id.name:

				order = Order.objects.create(order_date=order_date,
											 gym_id=select_gym,
											 myuser_id=user_logged,
											 hour_id=Hour.objects.get(id=s_hour_id),
											 total_price=s_total_price,
											 paid_money=s_paid_money,
											 status='Reserved',
											 description='رزرو شده توسظ مسئول منطقه')
				return redirect('Main:reservation', select_gym.slug)

			elif rol.name == 'سالن دار' and select_gym.user_id == request.user:
				order = Order.objects.create(order_date=order_date,
											 gym_id=select_gym,
											 myuser_id=user_logged,
											 hour_id=Hour.objects.get(id=s_hour_id),
											 total_price=s_total_price,
											 paid_money=s_paid_money,
											 status='Reserved',
											 description='رزرو شده توسظ سالن دار')
				return redirect('Main:reservation', select_gym.slug)

		context = {
			'day_of_week': day_of_week,
			'now': now,
			'select_gym': select_gym,
			'hours_open': hours_open,
			'hours': hours,
			'orders_count': orders_count,
			'orders': orders,
			'shanbe_e': shanbe_e,
			'shanbe': shanbe,
			'shanbe_t': shanbe_t,
			'yeshanbe_e': yeshanbe_e,
			'yeshanbe': yeshanbe,
			'yeshanbe_t': yeshanbe_t,
			'doshanbe_e': doshanbe_e,
			'doshanbe': doshanbe,
			'doshanbe_t': doshanbe_t,
			'seshanbe_e': seshanbe_e,
			'seshanbe': seshanbe,
			'seshanbe_t': seshanbe_t,
			'charshanbe_e': charshanbe_e,
			'charshanbe': charshanbe,
			'charshanbe_t': charshanbe_t,
			'panjshanbe_e': panjshanbe_e,
			'panjshanbe': panjshanbe,
			'panjshanbe_t': panjshanbe_t,
			'jome_e': jome_e,
			'jome': jome,
			'jome_t': jome_t,
			'reserve': True,
			's_day': s_day,
			's_description': s_description,
			's_gym_id': s_gym_id,
			's_hour_id': s_hour_id,
			's_myuser_id': s_myuser_id,
			's_order_date': s_order_date,
			's_paid_money': s_paid_money,
			's_status': s_status,
			's_total_price': s_total_price,

		}

		return render(request, 'modal_reserv.html', context)


def Add_Ticket(request):
	if request.user.is_authenticated:

		user_phone_number = request.user

		user_logged = MyUser.objects.get(phone_number=user_phone_number)
		roles_user = None
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		ticket_list1 = None

		for rol in roles_user:
			if rol.name == 'آموزش پرورش':
				ticket_list1 = Coach_Profile.objects.filter(user_id__group__name='آموزش و پرورش',
															user_id__city=user_logged.city)

				if roles_user_count == 0:
					ticket_list1 = Training_Class.objects.filter(user_id=user_logged)

				name = user_logged.name
				if request.method == 'POST':
					name = request.POST['name']
					family = request.POST['family_name']
					email = request.POST['email']
					title = request.POST['subject']  # title haman id 'girande ast
					text = request.POST['text']

					worker_req = Ticket.objects.create(name=name, family_name=family, myuser_id=user_logged,
													   email=email,
													   title=title, text=text)
					worker_req.save()

					return redirect('Main:add_ticket')
				else:

					context = {
						'roles_user_count': roles_user_count,
						'roles_user': roles_user,
						'ticket_list1': ticket_list1,
					}
					return render(request, 'role_panel/ticket.html', context)
			elif rol.name == 'مربی':

				if roles_user_count == 0:
					ticket_list1 = Training_Class.objects.filter(user_id=user_logged)

				name = user_logged.name
				if request.method == 'POST':
					name = request.POST['name']
					family = request.POST['family_name']
					email = request.POST['email']
					title = request.POST['subject']  # title haman id 'girande ast
					text = request.POST['text']

					worker_req = Ticket.objects.create(name=name, family_name=family, myuser_id=user_logged,
													   email=email,
													   title=title, text=text)
					worker_req.save()

					return redirect('Main:add_ticket')
				else:

					context = {
						'roles_user_count': roles_user_count,
						'roles_user': roles_user,
						'ticket_list1': ticket_list1,
					}
					return render(request, 'role_panel/ticket.html', context)
			elif rol.name == 'مسئول منطقه':

				if roles_user_count == 0:
					ticket_list1 = Training_Class.objects.filter(user_id=user_logged)

				name = user_logged.name
				if request.method == 'POST':
					name = request.POST['name']
					family = request.POST['family_name']
					email = request.POST['email']
					title = request.POST['subject']  # title haman id 'girande ast
					text = request.POST['text']
					tf = TicketForm(request.POST)
					if tf.is_valid():
						worker_req = Ticket.objects.create(name=name, family_name=family, myuser_id=user_logged,
														   email=email,
														   title=title, text=text)
						worker_req.save()

						return redirect('Main:add_ticket')
				else:

					context = {
						'roles_user_count': roles_user_count,
						'roles_user': roles_user,
						'ticket_list1': ticket_list1,
					}
					return render(request, 'role_panel/ticket.html', context)


			else:
				if request.method == 'POST':
					tf = TicketForm(request.POST)
					if tf.is_valid():
						name = request.POST['name']
						family = request.POST['family_name']
						email = request.POST['email']
						title = request.POST['subject']  # title haman id 'girande ast
						text = request.POST['text']
						tf = TicketForm(request.POST)

						worker_req = Ticket.objects.create(name=name, family_name=family,
														   email=email,
														   title=title, text=text)
						worker_req.save()

						context = {

						}
						return render(request, 'role_panel/ticket.html', context)
				else:

					context = {
						'roles_user_count': roles_user_count,
						'roles_user': roles_user
					}
					return render(request, 'role_panel/ticket.html', context)


def Work_Request(request):
	if request.user.is_authenticated:

		user_phone_number = request.user

		user_logged = MyUser.objects.get(phone_number=user_phone_number)
		roles_user = None
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		ticket_list1 = None

		for rol in roles_user:
			if rol.name == 'آموزش پرورش':
				ticket_list1 = MyUser.objects.filter(role__name='مربی', group__name='آموزش پرورش',
													 city=user_logged.city)
		if roles_user_count == 0:
			ticket_list1 = Training_Class.objects.filter(user_id=user_logged)

		name = user_logged.name
		if request.method == 'POST':
			name = request.POST['name']
			family = request.POST['family_name']
			email = request.POST['email']
			title = request.POST['subject']  # title haman id 'girande ast
			text = request.POST['text']
			tf = TicketForm(request.POST)
			if tf.is_valid():
				worker_req = Ticket.objects.create(name=name, family_name=family, myuser_id=user_logged, email=email,
												   title=title, text=text)
				worker_req.save()
				tf = TicketForm()
				context = {
					'tf': tf,
				}
				return redirect('Main:work_request')
		else:

			tf = TicketForm()

			context = {
				'roles_user_count': roles_user_count,
				'tf': tf,
				'ticket_list1': ticket_list1,
			}
			return render(request, 'worker.html', context)

	else:
		if request.method == 'POST':
			tf = TicketForm(request.POST)
			if tf.is_valid():
				name = request.POST['name']
				family = request.POST['family_name']
				email = request.POST['email']
				title = request.POST['subject']  # title haman id 'girande ast
				text = request.POST['text']
				tf = TicketForm(request.POST)

				worker_req = Ticket.objects.create(name=name, family_name=family,
												   email=email,
												   title=title, text=text)
				worker_req.save()
				tf = TicketForm()
				context = {
					'tf': tf,
				}
				return render(request, 'worker.html', context)
		else:

			tf = TicketForm()

			context = {
				'tf': tf,

			}
			return render(request, 'worker.html', context)


def Classes_List(request):
	if request.user.is_authenticated:

		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		user_province = user_logged_in.province
		if request.method == 'GET' and 'search_gym' in request.GET:
			province = request.GET.get('province', '')
			city = request.GET.get('city', '')
			area = request.GET.get('area', '')
			category = request.GET.get('category', '')
			sex = request.GET.get('sex', '')
			classes = Training_Class.objects.filter(gym_id__area_id__city_id__province_id__name=user_province)
			teachers = classes.select_related('coach_id').distinct('coach_id')

			classes = Training_Class.objects.filter(gym_id__area_id__name__contains=area,
													gym_id__area_id__city_id__name__contains=city,
													gym_id__area_id__city_id__province_id__name__contains=province,
													sex__contains=sex,
													category_id__name__contains=category)
			paginator = Paginator(classes, 10)
			page = request.GET.get('page')
			classes_list = paginator.get_page(page)

			areas = Area.objects.all()
			provinces = Province.objects.all()
			cities = City.objects.all()
			categories = Training_Class.objects.select_related('category_id').all().distinct('category_id')

			counter_comments = {}

			context = {
				'classes': classes_list,
				'counter_comments': counter_comments,
				'areas': areas,
				'provinces': provinces,
				'cities': cities,
				'teachers': teachers,
				'categories': categories,
			}
			return render(request, 'teaching.html', context)

		else:

			areas = Area.objects.all()
			provinces = Province.objects.all()
			cities = City.objects.all()
			categories = Training_Class.objects.select_related('category_id').all().distinct('category_id')

			counter_comments = {}

			classes = Training_Class.objects.filter(gym_id__area_id__city_id__province_id__name=user_province)
			paginator = Paginator(classes, 10)
			page = request.GET.get('page')
			classes_list = paginator.get_page(page)

			teachers = classes.select_related('coach_id').distinct('coach_id')
			for clas in classes:
				counter_comments[clas.gym_id.name] = Comment.objects.filter(gym_id__name=clas.gym_id.name).count()

			context = {
				'classes': classes_list,
				'counter_comments': counter_comments,
				'areas': areas,
				'provinces': provinces,
				'cities': cities,
				'teachers': teachers,
				'categories': categories,
			}
			return render(request, 'teaching.html', context)
	else:
		if request.method == 'GET' and 'search_gym' in request.GET:
			province = request.GET.get('province', '')
			city = request.GET.get('city', '')
			area = request.GET.get('area', '')
			category = request.GET.get('category', '')
			sex = request.GET.get('sex', '')
			classes = Training_Class.objects.all()
			teachers = classes.select_related('coach_id').distinct('coach_id')

			classes = Training_Class.objects.filter(gym_id__area_id__name__contains=area,
													gym_id__area_id__city_id__name__contains=city,
													gym_id__area_id__city_id__province_id__name__contains=province,
													category_id__name__contains=category)
			paginator = Paginator(classes, 10)
			page = request.GET.get('page')
			classes_list = paginator.get_page(page)

			areas = Area.objects.all()
			provinces = Province.objects.all()
			cities = City.objects.all()
			categories = Training_Class.objects.select_related('category_id').all().distinct('category_id')

			counter_comments = {}

			context = {
				'classes': classes_list,
				'counter_comments': counter_comments,
				'areas': areas,
				'provinces': provinces,
				'cities': cities,
				'teachers': teachers,
				'categories': categories,
			}
			return render(request, 'teaching.html', context)
		counter_comments = {}
		classes = Training_Class.objects.all()
		for clas in classes:
			counter_comments[clas.gym_id.name] = Comment.objects.filter(gym_id__name=clas.gym_id.name).count()

		areas = Area.objects.all()
		provinces = Province.objects.all()
		cities = City.objects.all()
		classes = Training_Class.objects.all()
		paginator = Paginator(classes, 10)
		page = request.GET.get('page')
		classes_list = paginator.get_page(page)

		categories = Training_Class.objects.select_related('category_id').all().distinct('category_id')
		teachers = Training_Class.objects.select_related('coach_id').all().distinct('coach_id')

		context = {
			'classes': classes_list,
			'counter_comments': counter_comments,
			'areas': areas,
			'provinces': provinces,
			'cities': cities,
			'teachers': teachers,
			'categories': categories,

		}
		return render(request, 'teaching.html', context)


def Training_Single(request, slug):
	if request.user.is_authenticated:
		select_training = Training_Class.objects.get(slug=slug)
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		context = {
			'user_logged_in': user_logged_in,
			'select_training': select_training
		}
		return render(request, 'coachpage.html', context)

	if request.method == 'POST' and 'reserve' in request.POST:
		return redirect('/Accounts/login/?next=/training_class_single/' + slug)
	select_training = Training_Class.objects.get(slug=slug)
	context = {
		'select_training': select_training
	}
	return render(request, 'coachpage.html', context)


def Dashboard(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':

				gyms = Gym.objects.all().order_by('area_id')
				paginator = Paginator(gyms, 10)
				page = request.GET.get('page')
				gyms_list = paginator.get_page(page)

				orders = Order.objects.filter(order_date__gte=datetime.today())
				gyms_counter = Gym.objects.all().count()
				users_counter = MyUser.objects.all().count()
				orders_counter = Order.objects.all().count()
				roles = Role.objects.all()
				teachers_counter = Role.objects.filter(name='مربی').count()
				context = {
					'gyms': gyms_list,
					'user_counter': users_counter,
					'roles': roles,
					'user_logged_in': user_logged_in,
					'orders_counter': orders_counter,
					'teachers_counter': teachers_counter,
					'gyms_counter': gyms_counter,
					'roles_user': roles_user,
					'orders': orders,
					'roles_user_count': roles_user_count,
					'superuser': True,
				}
				return render(request, 'role_panel/dashboard.html', context)
			elif role.name == 'آموزش پرورش':
				gyms = Gym.objects.filter(area_id__city_id__name=user_logged_in.city,
										  group__name='آموزش پرورش').order_by('area_id')
				paginator = Paginator(gyms, 10)
				page = request.GET.get('page')
				gyms_list = paginator.get_page(page)

				orders = Order.objects.filter(gym_id__area_id__city_id__name=user_logged_in.city,
											  order_date__gte=datetime.today())
				gyms_counter = Gym.objects.filter(area_id__city_id__name=user_logged_in.city,
												  group__name='آموزش پرورش').count()
				amoozesh_parvaresh = None
				try:
					amoozesh_parvaresh = Group.objects.get(name='آموزش پرورش')
				except:
					pass
				users_counter = None
				try:

					users_counter = MyUser.objects.filter(group=amoozesh_parvaresh, city=user_logged_in.city).count()
				except:
					pass
				orders_counter = Order.objects.filter(coupon_id__group_id__name='آموزش پرورش',
													  gym_id__area_id__city_id__name=user_logged_in.city).count()
				roles = Role.objects.all()
				teachers_counter = MyUser.objects.filter(role__name='مربی', city=user_logged_in.city).count()
				context = {
					'gyms': gyms_list,
					'user_counter': users_counter,
					'roles': roles,
					'user_logged_in': user_logged_in,
					'orders_counter': orders_counter,
					'teachers_counter': teachers_counter,
					'gyms_counter': gyms_counter,
					'roles_user': roles_user,
					'orders': orders,
					'roles_user_count': roles_user_count,
				}
				return render(request, 'role_panel/dashboard.html', context)
			elif role.name == 'سالن دار':
				orders = Order.objects.filter(gym_id__user_id=user_logged_in).order_by('order_date')
				paginator = Paginator(orders, 10)
				page = request.GET.get('page')
				orders_list = paginator.get_page(page)
				gym = Gym.objects.get(user_id=user_logged_in)
				users_counter = MyUser.objects.filter(order__gym_id=gym).distinct('phone_number').count()
				orders_counter = Order.objects.filter(gym_id__user_id=user_logged_in).count()
				teachers_counter = Coach_Profile.objects.filter(training_class__gym_id=gym).distinct('user_id').count()
				context = {
					'orders': orders_list,
					'user_counter': users_counter,
					'user_logged_in': user_logged_in,
					'orders_counter': orders_counter,
					'teachers_counter': teachers_counter,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count,

				}
				return render(request, 'role_panel/salondar_dashboard.html', context)

			elif role.name == 'مسئول منطقه':
				gyms = Gym.objects.filter(area_id__city_id__name=user_logged_in.city).order_by('area_id')
				paginator = Paginator(gyms, 10)
				page = request.GET.get('page')
				gyms_list = paginator.get_page(page)

				orders = Order.objects.filter(order_date__gte=datetime.today(),
											  gym_id__area_id__city_id__name=user_logged_in.city)
				gyms_counter = gyms.count()
				users = MyUser.objects.filter(city=user_logged_in.city).order_by('name')

				users_counter = users.count()
				orders_counter = orders.count()
				roles = Role.objects.all()
				teachers_counter = MyUser.objects.filter(role__name='مربی', city=user_logged_in.city).count()
				context = {
					'gyms': gyms_list,
					'user_counter': users_counter,
					'roles': roles,
					'user_logged_in': user_logged_in,
					'orders_counter': orders_counter,
					'teachers_counter': teachers_counter,
					'gyms_counter': gyms_counter,
					'roles_user': roles_user,
					'orders': orders,
					'roles_user_count': roles_user_count,
					'superuser': True,
				}
				return render(request, 'role_panel/dashboard.html', context)
			elif role.name == 'مربی':

				training_classes = Training_Class.objects.filter(coach_id__user_id=user_logged_in)
				student_count = MyUser.objects.filter(students__coach_id__user_id=user_logged_in).distinct('id').count()
				training_classes_count = training_classes.count()
				paginator = Paginator(training_classes, 10)
				page = request.GET.get('page')
				training_classes_list = paginator.get_page(page)

				context = {
					'student_count': student_count,
					'training_classes': training_classes_list,
					'user_logged_in': user_logged_in,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count,
					'training_classes_count': training_classes_count,
				}
				return render(request, 'role_panel/teacher_dashboard.html', context)
		orders = Order.objects.filter(myuser_id=user_logged_in)
		paginator = Paginator(orders, 10)
		page = request.GET.get('page')
		orders_list = paginator.get_page(page)
		context = {
			'orders': orders_list,
		}
		return render(request, 'role_panel/user_dashboard.html', context)

	else:
		return redirect('/Accounts/login/?next=/dashboard')


def Salon_Dar_Classes(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		for role in roles_user:
			if role.name == 'سالن دار':
				training_classes = Training_Class.objects.filter(gym_id__user_id=user_logged_in).order_by('date_start')
				paginator = Paginator(training_classes, 10)
				page = request.GET.get('page')
				training_classes_list = paginator.get_page(page)
				# gym = Gym.objects.get(user_id=user_logged_in)
				# users_counter = MyUser.objects.filter(order__gym_id=gym).distinct('phone_number').count()
				# orders_counter = Order.objects.filter(gym_id__user_id=user_logged_in).count()
				# teachers_counter = Coach_Profile.objects.filter(training_class__gym_id=gym).distinct('user_id').count()
				context = {
					'training_classes': training_classes_list,
					# 'user_counter': users_counter,
					'user_logged_in': user_logged_in,
					# 'orders_counter': orders_counter,
					# 'teachers_counter': teachers_counter,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count,

				}
				return render(request, 'role_panel/salondar_classes.html', context)
			else:
				return redirect('/Accounts/login/?next=/dashboard')


def User_Classes(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		classes = Training_Class.objects.filter(user_id=user_logged_in)
		context = {
			'training_classes': classes
		}
		return render(request, 'role_panel/salondar_classes.html', context)


def All_Users(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				users = MyUser.objects.all().order_by('name')
				paginator = Paginator(users, 10)
				page = request.GET.get('page')
				user_list = paginator.get_page(page)
				rols = Role.objects.all()
				groups = Group.objects.all()
				if request.method == 'POST':
					for group in groups:
						if group.name in request.POST:
							user_list = request.POST.getlist('select')
							d = ''
							for ids in user_list:
								d += ids
							list_split = d.split('Amir:D')
							for user in list_split:
								if user != '':
									user_select = None
									try:
										user_select = MyUser.objects.get(pk=user)
									except:
										user_select = None

									add_group = Group.objects.get(name=group.name)
									add_group.user_id.add(user_select)
									add_group.save()
							return redirect('Main:all_users')
					for role in rols:
						if role.name in request.POST:
							user_list = request.POST.getlist('select')
							d = ''
							for ids in user_list:
								d += ids
							list_split = d.split('Amir:D')
							for user in list_split:
								if user != '':
									user_select = None
									try:
										user_select = MyUser.objects.get(pk=user)
									except:
										user_select = None

									add_role = Role.objects.get(name=role.name)
									add_role.user_id.add(user_select)
									add_role.save()
							return redirect('Main:all_users')
				context = {
					'users': user_list,
					'rols': rols,
					'groups': groups,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'superuser': True
				}
				return render(request, 'role_panel/alluser.html', context)
			elif role.name == 'آموزش پرورش':
				users = MyUser.objects.filter(group__name='آموزش پرورش', city=user_logged_in.city).order_by('name')
				paginator = Paginator(users, 10)
				page = request.GET.get('page')
				user_list = paginator.get_page(page)
				rols = Role.objects.all()
				groups = Group.objects.all()
				if request.method == 'GET' and 'search_form' in request.GET:
					national_number = request.GET['national_number']
					phone_number = request.GET['phone_number']
					users = MyUser.objects.filter(Q(city=user_logged_in.city) & Q(national_number=national_number) | Q(
						city=user_logged_in.city) & Q(phone_number=phone_number))
					paginator = Paginator(users, 10)
					page = request.GET.get('page')
					user_list = paginator.get_page(page)
					rols = Role.objects.filter(name='آموزش پرورش')
					groups = Group.objects.filter(name='آموزش پرورش')
					context = {
						'groups': groups,
						'users': user_list,
						'roles_user_count': roles_user_count,
						'roles_user': roles_user
					}
					return render(request, 'role_panel/alluser.html', context)

				if request.method == 'POST':

					for group in groups:
						if group.name in request.POST:
							user_list = request.POST.getlist('select')
							d = ''
							for ids in user_list:
								d += ids
							list_split = d.split('Amir:D')
							for user in list_split:
								if user != '':
									user_select = None
									try:
										user_select = MyUser.objects.get(pk=user)
									except:
										user_select = None

									add_group = Group.objects.get(name=group.name)
									add_group.user_id.add(user_select)
									add_group.save()
							return redirect('Main:all_users')
					for role in rols:
						if role.name in request.POST:
							user_list = request.POST.getlist('select')
							d = ''
							for ids in user_list:
								d += ids
							list_split = d.split('Amir:D')
							for user in list_split:
								if user != '':
									user_select = None
									try:
										user_select = MyUser.objects.get(pk=user)
									except:
										user_select = None

									add_role = Role.objects.get(name=role.name)
									add_role.user_id.add(user_select)
									add_role.save()
							return redirect('Main:all_users')

				groups = Group.objects.filter(name='آموزش پرورش')
				context = {
					'users': user_list,
					'groups': groups,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,

				}
				return render(request, 'role_panel/alluser.html', context)


			elif role.name == 'مسئول منطقه':

				users = MyUser.objects.filter(city=user_logged_in.city).order_by('name')
				paginator = Paginator(users, 10)
				page = request.GET.get('page')
				user_list = paginator.get_page(page)
				rols = Role.objects.all()
				groups = Group.objects.all()
				if request.method == 'POST':
					for group in groups:
						if group.name in request.POST:
							user_list = request.POST.getlist('select')
							d = ''
							for ids in user_list:
								d += ids
							list_split = d.split('Amir:D')
							for user in list_split:
								if user != '':
									user_select = None
									try:
										user_select = MyUser.objects.get(pk=user)
									except:
										user_select = None

									add_group = Group.objects.get(name=group.name)
									add_group.user_id.add(user_select)
									add_group.save()
							return redirect('Main:all_users')
					for role in rols:
						if role.name in request.POST:
							user_list = request.POST.getlist('select')
							d = ''
							for ids in user_list:
								d += ids
							list_split = d.split('Amir:D')
							for user in list_split:
								if user != '':
									user_select = None
									try:
										user_select = MyUser.objects.get(pk=user)
									except:
										user_select = None

									add_role = Role.objects.get(name=role.name)
									add_role.user_id.add(user_select)
									add_role.save()
							return redirect('Main:all_users')

				groups = Group.objects.all()
				context = {
					'users': user_list,
					'groups': groups,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,

				}
				return render(request, 'role_panel/alluser.html', context)

			return redirect('Main:dashboard')
	else:
		return redirect('/Accounts/login/?next=/dashboard/all_users')


def Delete_Role_Group(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser' or role.name == 'مسئول منطقه':

				if request.method == 'GET' and 'search_form' in request.GET:
					national_number = request.GET['national_number']
					phone_number = request.GET['phone_number']
					users = MyUser.objects.filter(Q(city=user_logged_in.city) & Q(national_number=national_number) | Q(
						city=user_logged_in.city) & Q(phone_number=phone_number))
					rols = Role.objects.filter(name='آموزش پرورش')
					groups = Group.objects.filter(name='آموزش پرورش')
					context = {
						'groups': groups,
						'rols': rols,
						'users': users,
						'roles_user_count': roles_user_count,
						'roles_user': roles_user
					}
					return render(request, 'role_panel/deletuser.html', context)

				if request.method == 'POST' and 'delete_form' in request.POST:
					if request.POST.getlist('roll'):
						user_list = request.POST.getlist('roll')
						d = ''
						for ids in user_list:
							d += ids
						list_split = d.split('Amir:D')

						for user_id in list_split:
							if user_id != '':
								user = MyUser.objects.get(pk=user_id)
								delete_roles = Role.objects.filter(user_id=user)
								for delete_role in delete_roles:
									if role.name == 'مسئول منطقه':
										if delete_role.name == 'superuser':
											return redirect('Main:delete_role_group')
									else:
										delete_role.user_id.remove(user)
								for delete_role in delete_roles:
									if role.name == 'مسئول منطقه':
										delete_role.user_id.remove(user)
						return redirect('Main:delete_role_group')
					if request.POST.getlist('groupp'):
						user_list = request.POST.getlist('groupp')
						d = ''
						for ids in user_list:
							d += ids
							list_split = d.split('Amir:D')

							for user_id in list_split:
								if user_id != '':
									user = MyUser.objects.get(pk=user_id)
									delete_groups = Group.objects.filter(user_id=user)
									for delete_group in delete_groups:
										delete_group.user_id.remove(user)
							return redirect('Main:delete_role_group')
					if request.POST.getlist('select_user'):
						user_list = request.POST.getlist('select_user')
						d = ''
						for ids in user_list:
							d += ids
							list_split = d.split('Amir:D')

							for user_id in list_split:
								if user_id != '':
									delete_user = MyUser.objects.get(pk=user_id)
									delete_user.delete()
							return redirect('Main:delete_role_group')
				users = MyUser.objects.all()
				rols = Role.objects.all()
				groups = Group.objects.all()
				context = {
					'groups': groups,
					'rols': rols,
					'users': users,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'superuser': True

				}
				return render(request, 'role_panel/deletuser.html', context)
			elif role.name == 'آموزش پرورش':

				if request.method == 'GET' and 'search_form' in request.GET:
					national_number = request.GET['national_number']
					phone_number = request.GET['phone_number']
					users = MyUser.objects.filter(Q(city=user_logged_in.city) & Q(group__name='آموزش پرورش') & Q(
						national_number=national_number) | Q(city=user_logged_in.city) & Q(
						phone_number=phone_number) & Q(group__name='آموزش پرورش'))
					rols = Role.objects.filter(name='آموزش پرورش')
					groups = Group.objects.filter(name='آموزش پرورش')
					context = {
						'groups': groups,
						'rols': rols,
						'users': users,
						'roles_user_count': roles_user_count,
						'roles_user': roles_user
					}
					return render(request, 'role_panel/deletuser.html', context)

				if request.method == 'POST' and 'delete_form' in request.POST:
					if request.POST.getlist('roll'):
						user_list = request.POST.getlist('roll')
						d = ''
						for ids in user_list:
							d += ids
						list_split = d.split('Amir:D')

						for user_id in list_split:
							if user_id != '':
								user = MyUser.objects.get(pk=user_id)
								delete_roles = Role.objects.filter(user_id=user)
								for delete_role in delete_roles:
									if delete_role.name == 'مسئول منطقه' or delete_role.name == 'superuser':
										return redirect('Main:delete_role_group')
								for delete_role in delete_roles:
									delete_role.user_id.remove(user)
						return redirect('Main:delete_role_group')
					if request.POST.getlist('groupp'):
						user_list = request.POST.getlist('groupp')
						d = ''
						for ids in user_list:
							d += ids
							list_split = d.split('Amir:D')

							for user_id in list_split:
								if user_id != '':
									user = MyUser.objects.get(pk=user_id)
									delete_group = Group.objects.get(user_id=user, name='آموزش پرورش')

									delete_group.user_id.remove(user)
							return redirect('Main:delete_role_group')
					if request.POST.getlist('select_user'):
						user_list = request.POST.getlist('select_user')
						d = ''
						for ids in user_list:
							d += ids
							list_split = d.split('Amir:D')

							for user_id in list_split:
								if user_id != '':
									delete_user = MyUser.objects.get(pk=user_id)
									delete_user.delete()
							return redirect('Main:delete_role_group')
				users = MyUser.objects.filter(group__name='آموزش پرورش', city=user_logged_in.city)
				rols = Role.objects.filter(name='آموزش پرورش')
				groups = Group.objects.filter(name='آموزش پرورش')
				context = {
					'groups': groups,
					'rols': rols,
					'users': users,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user
				}
				return render(request, 'role_panel/deletuser.html', context)

	else:
		return redirect('/Accounts/login/?next=/dashboard/delete_role_group')


def Edite_Gym_info(request):
	gyms = Gym.objects.all()

	return render(request, 'all_gyms.html', locals())


def Add_Facility(request):
	if request.method == 'POST' and 'facility_add' in request.POST:
		facility = request.POST['facility_add']
		add_facility = Facility.objects.create(name=facility)
		return redirect('Main:add_facility')

	if request.method == 'POST' and 'ids' in request.POST:
		ids = request.POST.getlist('ids')
		str = ''
		for id in ids:
			str += id
		str = str.split('Amir:D')
		for id in str:
			if id != '':
				facility = Facility.objects.get(pk=id)
				facility.delete()
		return redirect('Main:add_facility')

	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				facilities = Facility.objects.all()
				context = {
					'facilities': facilities,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count
				}
				return render(request, 'role_panel/newfacility.html', context)
			else:
				return redirect('Main:dashboard')
	else:
		return HttpResponse('/Accounts/login/?next=/dashboard/add_facility/')


def Add_province(request):
	if request.method == 'POST' and 'province_add' in request.POST:  # for add
		province = request.POST['province_add']
		try:
			add_province = Province.objects.get(name=province)
		except:
			add_province = Province.objects.create(name=province)
		return redirect('Main:add_province')

	if request.method == 'POST' and 'ids' in request.POST:  # for delete
		ids = request.POST.getlist('ids')
		str = ''
		for id in ids:
			str += id
		str = str.split('Amir:D')
		for id in str:
			if id != '':
				province = Province.objects.get(pk=id)
				try:
					province.delete()
				except:
					pass
		return redirect('Main:add_province')

	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				provinces = Province.objects.all()
				# paginator = Paginator(provinces, 2)
				# page = request.GET.get('page')
				# provinces = paginator.get_page(page)
				context = {
					'provinces': provinces,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count
				}
				return render(request, 'role_panel/newprovince.html', context)
			else:
				return redirect('Main:dashboard')
	else:
		return HttpResponse('/Accounts/login/?next=/dashboard/add_province/')


def Add_city(request):
	if request.method == 'POST' and 'city_add' in request.POST:
		city = request.POST['city_add']
		province_id = request.POST['province']
		try:
			add_city = City.objects.get(province_id__id=province_id, name=city)
		except:
			add_city = City.objects.create(province_id_id=province_id, name=city)
		return redirect('Main:add_city')

	if request.method == 'POST' and 'ids' in request.POST:
		ids = request.POST.getlist('ids')
		str = ''
		for id in ids:
			str += id
		str = str.split('Amir:D')
		for id in str:
			if id != '':
				city = City.objects.get(pk=id)
				try:
					city.delete()
				except:
					pass
		return redirect('Main:add_city')

	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				cities = City.objects.all().order_by('province_id__name')
				provinces = Province.objects.all().order_by('name')
				context = {
					'cities': cities,
					'provinces': provinces,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user
				}
				return render(request, 'role_panel/newcity.html', context)


def Add_area(request):
	if request.method == 'POST' and 'area_add' in request.POST:
		area = request.POST['area_add']
		province_id = request.POST['city']
		try:
			add_area = Area.objects.get(city_id__id=province_id, name=area)
		except:
			add_area = City.objects.create(city_id_id=province_id, name=area)
		return redirect('Main:add_area')

	if request.method == 'POST' and 'ids' in request.POST:
		ids = request.POST.getlist('ids')
		str = ''
		for id in ids:
			str += id
		str = str.split('Amir:D')
		for id in str:
			if id != '':
				area = Area.objects.get(pk=id)
				try:
					area.delete()
				except:
					pass
		return redirect('Main:add_area')

	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				areas = Area.objects.all().order_by('city_id__name')
				cities = City.objects.all().order_by('name')
				context = {
					'cities': cities,
					'areas': areas,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user
				}
				return render(request, 'role_panel/neware.html', context)


def Add_gym_type(request):
	if request.method == 'POST' and 'gym_type_add' in request.POST:
		gym_type = request.POST['gym_type_add']
		try:
			add_gym_type = Category.objects.get(name=gym_type)
		except:
			add_gym_type = Category.objects.create(name=gym_type)
		return redirect('Main:add_gym_type')

	if request.method == 'POST' and 'ids' in request.POST:
		ids = request.POST.getlist('ids')
		str = ''
		for id in ids:
			str += id
		str = str.split('Amir:D')
		for id in str:
			if id != '':
				category = Category.objects.get(pk=id)
				try:
					category.delete()
				except:
					pass
		return redirect('Main:add_gym_type')

	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				gym_types = Category.objects.all()
				# paginator = Paginator(provinces, 2)
				# page = request.GET.get('page')
				# provinces = paginator.get_page(page)
				context = {
					'gym_types': gym_types,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count
				}
				return render(request, 'role_panel/gymcategory.html', context)
			else:
				return redirect('Main:dashboard')
	else:
		return HttpResponse('/Accounts/login/?next=/dashboard/add_category/')


def Teachers(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				rol = Role.objects.get(name='مربی')
				teachers = MyUser.objects.filter(role=rol)

				context = {
					'teachers': teachers,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'superuser': True

				}
				return render(request, 'role_panel/teachers.html', context)
			elif role.name == 'آموزش پرورش':
				teachers = MyUser.objects.filter(role__name='مربی', group__name='آموزش پرورش', city=user_logged_in.city)

				context = {
					'teachers': teachers,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user
				}
				return render(request, 'role_panel/teachers.html', context)

			elif role.name == 'مسئول منطقه':
				teachers = MyUser.objects.filter(role__name='مربی', city=user_logged_in.city)

				context = {
					'teachers': teachers,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user
				}
				return render(request, 'role_panel/teachers.html', context)


def Teachers_Details(request, slug):
	select_user = MyUser.objects.get(pk=slug)
	try:
		coach = Coach_Profile.objects.get(user_id=select_user)
	except:
		coach = Coach_Profile.objects.create(user_id=select_user)
	if request.method == 'POST' and 'save_form' in request.POST:

		name = request.POST['name']
		department_name = request.POST['department_name']
		job = request.POST['job']
		national_number = request.POST['national_number']
		text = request.POST['text']
		phone_number = request.POST['phone_number']

		try:
			picture = request.FILES['picture']
		except:
			picture = coach.picture
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		select_user.national_number = national_number
		select_user.phone_number = phone_number
		select_user.name = name
		try:
			select_user.save()
		except:
			context = {
				'error': True,
				'message': 'کد ملی وارد شده صحیح نیست.',
				'select_user': select_user,
				'coach': coach,
				'roles_user': roles_user,
				'roles_user_count': roles_user_count
			}
			return render(request, 'role_panel/teacher_profile.html', context)
		coach = Coach_Profile.objects.get(user_id=select_user)

		coach.job = job
		coach.text = text
		coach.department_name = department_name
		coach.picture = picture
		coach.save()

		return redirect('Main:teachers_details', select_user.id)

	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			if role.name == 'superuser':
				select_user = MyUser.objects.get(pk=slug)

				coach = Coach_Profile.objects.get(user_id=select_user)

				context = {
					'select_user': select_user,
					'coach': coach,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count
				}
				return render(request, 'role_panel/teacher_profile.html', context)
			elif role.name == 'مسئول منطقه':
				select_user = MyUser.objects.get(pk=slug)

				coach = Coach_Profile.objects.get(user_id=select_user)

				context = {
					'select_user': select_user,
					'coach': coach,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count
				}
				return render(request, 'role_panel/teacher_profile.html', context)


def Requests(request):
	if request.user.is_authenticated:
		user_phone_number = request.user
		user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
		roles_user_count = 0
		try:
			roles_user = Role.objects.filter(user_id=user_logged_in)
			roles_user_count = roles_user.count()
		except Role.DoesNotExist:
			roles_user = None

		# admin access
		for role in roles_user:
			requests = None
			if role.name == 'superuser':
				requests = Ticket.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'requests': requests,
				}
				return render(request, 'role_panel/requests.html', context)

			elif role.name == 'آموزش پرورش' or role.name == 'مسئول منطقه':
				requests = Ticket.objects.filter(title='amoozesh', myuser_id__city=user_logged_in.city)
				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'requests': requests,
				}
				return render(request, 'role_panel/requests.html', context)

			elif role.name == 'مربی':
				requests = Ticket.objects.filter(title=user_logged_in.id, myuser_id__city=user_logged_in.city)
				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'requests': requests,
				}
				return render(request, 'role_panel/requests.html', context)
			context = {
				'roles_user_count': roles_user_count,
				'roles_user': roles_user,
				'requests': requests,
			}
			return render(request, 'role_panel/requests.html', context)


def Edit_Profile_Teacher(request):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(id__exact=request.user.id)

		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()
		for role in roles_user:
			if role.name == 'مربی':
				coach_profiles = Coach_Profile.objects.all()

				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					department_name = request.POST['department_name']
					job = request.POST['job']
					national_number = request.POST['national_number']
					text = request.POST['text']
					phone_number = request.POST['phone_number']
					picture = request.FILES['picture']

					user_logged_in.national_number = national_number
					user_logged_in.phone_number = phone_number
					user_logged_in.name = name

					user_logged_in.save()
					user_profile = None
					try:
						user_profile = Coach_Profile.objects.get(user_id=user_logged_in)
					except:
						user_profile = Coach_Profile.objects.create(user_id=user_logged_in)
					user_profile.job = job
					user_profile.text = text
					user_profile.department_name = department_name
					user_profile.picture = picture
					user_profile.save()

					return redirect('Main:edit_profile')

				try:
					coach = Coach_Profile.objects.get(user_id=user_logged_in)
				except:
					user_profile = Coach_Profile.objects.create(user_id=user_logged_in)
					coach = Coach_Profile.objects.get(user_id=user_logged_in)

				context = {
					'coach': coach,
					'coach_profiles': coach_profiles,
					'roles_user_count': roles_user_count,
					'roles_user': roles_user

				}

				return render(request, 'couchprofile.html', context)
		return redirect('Main:dashboard')
	else:
		return redirect('/Accounts/login/?next=/dashboard/edit_profile/')


def Students(request):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()
		all_user = MyUser.objects.all()
		class_users = {}
		users = []
		for role in roles_user:
			if role.name == 'مربی':
				training_classes = Training_Class.objects.filter(coach_id__user_id=user_logged_in)
				for training_class in training_classes:  # 2D array
					st = MyUser.objects.filter(students=training_class)
					for student in st:
						users.append(student.phone_number)
					class_users[training_class.name] = users
					users = []

				context = {
					'class_users': class_users,
					'all_user': all_user,
					'roles_user': roles_user,
					'roles_user_count': roles_user_count
				}
				return render(request, 'students.html', context)
			else:
				return redirect('Main:dashboard')
	else:
		return redirect('Accounts/login/?next=/dashboardAccounts/login/?next=/dashboard/students/')


def Select_Gym(request):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()

		for role in roles_user:
			if role.name == 'مربی':
				if request.method == 'POST' and 'gym_id' in request.POST:
					gym_id = request.POST['gym_id']
					select_gym = None
					try:
						select_gym = Gym.objects.get(id=gym_id)
					except:
						return render(request, 'role_panel/select-gym-new-class.html', context={
							'error': True,
							'message': 'لطفا سالن را به درستی انتخاب کنید.'
						})
					return redirect('Main:add_class', select_gym.id)
				gyms = Gym.objects.filter(area_id__city_id__name=user_logged_in.city)
				coaches = Coach_Profile.objects.all()
				categories = Category.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
				}
				return render(request, 'role_panel/select-gym-new-class.html', context)

			elif role.name == 'superuser':
				if request.method == 'POST' and 'gym_id' in request.POST:
					gym_id = request.POST['gym_id']
					select_gym = None
					try:
						select_gym = Gym.objects.get(id=gym_id)
					except:
						return render(request, 'role_panel/select-gym-new-class.html', context={
							'roles_user_count': roles_user_count,
							'roles_user': roles_user,
							'error': True,
							'message': 'لطفا سالن را به درستی انتخاب کنید.'
						})
					return redirect('Main:add_class', select_gym.id)

				gyms = Gym.objects.all()
				coaches = Coach_Profile.objects.all()
				categories = Category.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
				}
				return render(request, 'role_panel/select-gym-new-class.html', context)

			else:
				return redirect('Main:dashboard')
	else:
		return redirect('Accounts/login/?next=/dashboard/select_gym/')


def Add_Class(request, slug):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()

		for role in roles_user:
			if role.name == 'superuser':
				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					coach_id = request.POST['coach_id']
					hour_id = request.POST['hour_id']
					number_of_session = request.POST['number_of_session']
					price = request.POST['price']
					start_date = request.POST['start_date']
					end_date = request.POST['end_date']
					category_id = request.POST['category_id']
					picture = request.FILES['picture']
					text = request.POST['text']
					sex = request.POST['sex']

					start_date = datetime.strptime(start_date, '%Y-%m-%d')
					end_date = datetime.strptime(end_date, '%Y-%m-%d')
					coach_id = Coach_Profile.objects.get(id=coach_id)
					gym_id = Gym.objects.get(id=slug)
					category_id = Category.objects.get(id=category_id)
					hour_id = Hour.objects.get(id=hour_id)
					day = hour_id.day
					numday = None

					if day == 'doshanbe':
						numday = 0
					elif day == 'seshanbe':
						numday = 1
					elif day == 'charshanbe':
						numday = 2
					elif day == 'panjshanbe':
						numday = 3
					elif day == 'jome':
						numday = 4
					elif day == 'shanbe':
						numday = 5
					elif day == 'yeshanbe':
						numday == 6

					cstart_date = start_date
					cend_date = end_date
					amir = True
					while (amir):
						if cstart_date <= cend_date:

							if cstart_date.weekday() == numday:
								try:
									Order.objects.get(order_date=cstart_date,
													  gym_id=gym_id, hour_id=hour_id,
													  )
									gyms = Gym.objects.all()
									coaches = Coach_Profile.objects.all()
									categories = Category.objects.all()
									hours = Hour.objects.filter(gym_id__id=slug).order_by('open')
									context = {
										'error': True,
										'message': 'چند تایم های انتخابی از قبل رزرو شده اند.',
										'roles_user_count': roles_user_count,
										'roles_user': roles_user,
										'hours': hours,
										'coaches': coaches,
										'gyms': gyms,
										'categories': categories,
									}
									return render(request, 'role_panel/new-class.html', context)
								except:
									pass
							cstart_date = cstart_date + timedelta(days=1)
						else:
							amir = False

					Training_Class.objects.create(name=name, coach_id=coach_id, gym_id=gym_id,
												  number_of_session=number_of_session, price=price,
												  date_start=start_date, date_expire=end_date,
												  category_id=category_id, picture=picture, hour_id=hour_id, text=text,
												  sex=sex)

					return redirect('Main:add_class', slug)

				gyms = Gym.objects.all()
				coaches = Coach_Profile.objects.all()
				categories = Category.objects.all()
				hours = Hour.objects.filter(gym_id__id=slug).order_by('open')

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'hours': hours,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
				}
				return render(request, 'role_panel/new-class.html', context)
			elif role.name == 'مربی':
				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					coach_id = request.POST['coach_id']
					hour_id = request.POST['hour_id']
					number_of_session = request.POST['number_of_session']
					price = request.POST['price']
					start_date = request.POST['start_date']
					end_date = request.POST['end_date']
					category_id = request.POST['category_id']
					picture = request.FILES['picture']
					text = request.POST['text']
					sex = request.POST['sex']

					start_date = datetime.strptime(start_date, '%Y-%m-%d')
					end_date = datetime.strptime(end_date, '%Y-%m-%d')
					coach_id = Coach_Profile.objects.get(id=coach_id)
					gym_id = Gym.objects.get(id=slug)
					category_id = Category.objects.get(id=category_id)
					hour_id = Hour.objects.get(id=hour_id)

					day = hour_id.day
					numday = None

					if day == 'doshanbe':
						numday = 0
					elif day == 'seshanbe':
						numday = 1
					elif day == 'charshanbe':
						numday = 2
					elif day == 'panjshanbe':
						numday = 3
					elif day == 'jome':
						numday = 4
					elif day == 'shanbe':
						numday = 5
					elif day == 'yeshanbe':
						numday == 6

					cstart_date = start_date
					cend_date = end_date
					amir = True
					while (amir):
						if cstart_date <= cend_date:

							if cstart_date.weekday() == numday:
								try:
									Order.objects.get(order_date=cstart_date,
													  gym_id=gym_id, hour_id=hour_id,
													  )
									gyms = Gym.objects.all()
									coaches = Coach_Profile.objects.all()
									categories = Category.objects.all()
									hours = Hour.objects.filter(gym_id__id=slug).order_by('open')
									context = {
										'error': True,
										'message': 'تایم های انتخابی از قبل رزرو شده اند.',
										'roles_user_count': roles_user_count,
										'roles_user': roles_user,
										'hours': hours,
										'coaches': coaches,
										'gyms': gyms,
										'categories': categories,
									}
									return render(request, 'role_panel/new-class.html', context)
								except:
									pass
							cstart_date = cstart_date + timedelta(days=1)
						else:
							amir = False

					Training_Class.objects.create(name=name, coach_id=coach_id, gym_id=gym_id,
												  number_of_session=number_of_session, price=price,
												  date_start=start_date, date_expire=end_date,
												  category_id=category_id, picture=picture, hour_id=hour_id, text=text,
												  sex=sex)

					return redirect('Main:add_class', slug)

				gyms = Gym.objects.filter(area_id__name=user_logged_in.area)
				coaches = Coach_Profile.objects.filter(user_id=user_logged_in)
				categories = Category.objects.all()
				hours = Hour.objects.filter(gym_id__id=slug).order_by('open')

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'hours': hours,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
				}
				return render(request, 'role_panel/new-class.html', context)


			else:
				return redirect('Main:dashboard')

		context = {
			'roles_user_count': roles_user_count,
			'roles_user': roles_user,

		}
		return render(request, 'role_panel/select-gym-new-class.html', context)


def Edit_class(request, slug):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()
		select_training = Training_Class.objects.get(id=slug)

		for role in roles_user:
			if role.name == 'سالن دار':
				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					coach_id = request.POST['coach_id']
					hour_id = request.POST['hour_id']
					number_of_session = request.POST['number_of_session']
					price = request.POST['price']
					start_date = request.POST['start_date']
					end_date = request.POST['end_date']
					category_id = request.POST['category_id']
					picture = request.FILES['picture']
					text = request.POST['text']
					sex = request.POST['sex']

					start_date = datetime.strptime(start_date, '%Y-%m-%d')
					end_date = datetime.strptime(end_date, '%Y-%m-%d')
					coach_id = Coach_Profile.objects.get(id=coach_id)
					gym_id = Gym.objects.get(id=select_training.gym_id.id)
					category_id = Category.objects.get(id=category_id)
					hour_id = Hour.objects.get(id=hour_id)
					select_training = Training_Class.objects.get(id=slug)
					select_training.name = name
					select_training.coach_id = coach_id
					select_training.gym_id = gym_id
					select_training.number_of_session = number_of_session
					select_training.price = price
					select_training.date_start = start_date
					select_training.date_expire = end_date
					select_training.category_id = category_id
					select_training.picture = picture
					select_training.hour_id = hour_id
					select_training.text = text
					select_training.sex = sex
					select_training.save()
					return redirect('Main:edit_class', slug)

				select_training = Training_Class.objects.get(id=slug)

				gyms = Gym.objects.all()
				coaches = Coach_Profile.objects.filter(user_id=user_logged_in)
				categories = Category.objects.all()
				hours = Hour.objects.filter(gym_id=select_training.gym_id).order_by('open')
				start = datetime.strftime(select_training.date_start, '%Y-%m-%d')
				end = datetime.strftime(select_training.date_expire, '%Y-%m-%d')

				context = {
					'start': start,
					'end': end,
					'select_training': select_training,
					'hours': hours,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
					'edit': True,
				}
				return render(request, 'role_panel/new-class.html', context)


def Add_Gym(request):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()

		for role in roles_user:
			if role.name == 'مسئول منطقه':
				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					area_id = request.POST['area_id']
					address = request.POST['address']
					picture = request.FILES['picture']
					status = request.POST['status']
					phone = request.POST['phone']
					description = request.POST['text']
					sex = request.POST['sex']
					user_id = request.POST['user_id']
					category_id = request.POST['category_id']

					area_id = Area.objects.get(id=area_id)
					user_id = MyUser.objects.get(id=user_id)
					select_gym = Gym(name=name, area_id=area_id, address=address, picture=picture, status=status,
									 phone=phone, description=description, sex=sex, user_id=user_id)
					select_gym.save()

					category_list = request.POST.getlist('category_id')
					d = ''
					for ids in category_list:
						d += ids
					list_split = d.split('Amir:D')
					for category in list_split:
						if category != '':
							category_select = None
							try:
								category_select = Category.objects.get(pk=category)
							except:
								category_select = None

							select_gym.category_id.add(category_select)
							select_gym.save()

					facility_list = request.POST.getlist('facility_id')
					d = ''
					for ids in facility_list:
						d += ids
					list_split = d.split('Amir:D')
					for facility in list_split:
						if facility != '':
							facility_select = None
							try:
								facility_select = Facility.objects.get(pk=facility)
							except:
								facility_select = None

							select_gym.facility_id.add(facility_select)
							select_gym.save()

					select_gym.save()

					# areas = Area.objects.filter(city_id__name=user_logged_in.city)
					# users = MyUser.objects.filter(phone_number=request.user)
					# categories = Category.objects.all()
					# facilities = Facility.objects.all()
					#
					# context = {
					# 	'areas': areas,
					# 	'users': users,
					# 	'categories': categories,
					# 	'facilities': facilities,
					# 	'edit': True,
					# 	'select_gym':select_gym,
					# }
					return redirect('Main:add_gym')
				areas = Area.objects.filter(city_id__name=user_logged_in.city)
				users = MyUser.objects.filter(phone_number=request.user)
				categories = Category.objects.all()
				facilities = Facility.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'areas': areas,
					'users': users,
					'categories': categories,
					'facilities': facilities,
				}
				return render(request, 'role_panel/new_gym.html', context)

			elif role.name == 'superuser':
				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					area_id = request.POST['area_id']
					address = request.POST['address']
					picture = request.FILES['picture']
					status = request.POST['status']
					phone = request.POST['phone']
					description = request.POST['text']
					sex = request.POST['sex']
					user_id = request.POST['user_id']
					category_id = request.POST['category_id']

					area_id = Area.objects.get(id=area_id)
					user_id = MyUser.objects.get(id=user_id)
					select_gym = Gym(name=name, area_id=area_id, address=address, picture=picture, status=status,
									 phone=phone, description=description, sex=sex, user_id=user_id)
					select_gym.save()

					category_list = request.POST.getlist('category_id')
					d = ''
					for ids in category_list:
						d += ids
					list_split = d.split('Amir:D')
					for category in list_split:
						if category != '':
							category_select = None
							try:
								category_select = Category.objects.get(pk=category)
							except:
								category_select = None

							select_gym.category_id.add(category_select)
							select_gym.save()

					facility_list = request.POST.getlist('facility_id')
					d = ''
					for ids in facility_list:
						d += ids
					list_split = d.split('Amir:D')
					for facility in list_split:
						if facility != '':
							facility_select = None
							try:
								facility_select = Facility.objects.get(pk=facility)
							except:
								facility_select = None

							select_gym.facility_id.add(facility_select)
							select_gym.save()

					select_gym.save()

					# areas = Area.objects.filter(city_id__name=user_logged_in.city)
					# users = MyUser.objects.filter(phone_number=request.user)
					# categories = Category.objects.all()
					# facilities = Facility.objects.all()
					#
					# context = {
					# 	'areas': areas,
					# 	'users': users,
					# 	'categories': categories,
					# 	'facilities': facilities,
					# 	'edit': True,
					# 	'select_gym':select_gym,
					# }
					return redirect('Main:add_gym')

				areas = Area.objects.all().order_by('city_id__province_id__name')
				users = MyUser.objects.all()
				categories = Category.objects.all()
				facilities = Facility.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'areas': areas,
					'users': users,
					'categories': categories,
					'facilities': facilities,
				}
				return render(request, 'role_panel/new_gym.html', context)
			elif role.name == 'آموزش پرورش':
				if request.method == 'POST' and 'save_form' in request.POST:
					name = request.POST['name']
					area_id = request.POST['area_id']
					address = request.POST['address']
					picture = request.FILES['picture']
					status = request.POST['status']
					phone = request.POST['phone']
					description = request.POST['text']
					sex = request.POST['sex']
					user_id = request.POST['user_id']
					category_id = request.POST['category_id']

					area_id = Area.objects.get(id=area_id)
					user_id = MyUser.objects.get(id=user_id)
					select_gym = Gym(name=name, area_id=area_id, address=address, picture=picture, status=status,
									 phone=phone, description=description, sex=sex, user_id=user_id)
					select_gym.save()

					category_list = request.POST.getlist('category_id')
					d = ''
					for ids in category_list:
						d += ids
					list_split = d.split('Amir:D')
					for category in list_split:
						if category != '':
							category_select = None
							try:
								category_select = Category.objects.get(pk=category)
							except:
								category_select = None

							select_gym.category_id.add(category_select)
							select_gym.save()

					facility_list = request.POST.getlist('facility_id')
					d = ''
					for ids in facility_list:
						d += ids
					list_split = d.split('Amir:D')
					for facility in list_split:
						if facility != '':
							facility_select = None
							try:
								facility_select = Facility.objects.get(pk=facility)
							except:
								facility_select = None

							select_gym.facility_id.add(facility_select)
							select_gym.save()

					select_gym.save()

					# areas = Area.objects.filter(city_id__name=user_logged_in.city)
					# users = MyUser.objects.filter(phone_number=request.user)
					# categories = Category.objects.all()
					# facilities = Facility.objects.all()
					#
					# context = {
					# 	'areas': areas,
					# 	'users': users,
					# 	'categories': categories,
					# 	'facilities': facilities,
					# 	'edit': True,
					# 	'select_gym':select_gym,
					# }
					return redirect('Main:add_gym')

				areas = Area.objects.filter(city_id__name=user_logged_in.city)
				users = MyUser.objects.filter(phone_number=request.user)
				categories = Category.objects.all()
				facilities = Facility.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'areas': areas,
					'users': users,
					'categories': categories,
					'facilities': facilities,
				}
				return render(request, 'role_panel/new_gym.html', context)


def Select_Gym_add_hour(request):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()

		for role in roles_user:
			if role.name == 'مربی':
				if request.method == 'POST' and 'gym_id' in request.POST:
					gym_id = request.POST['gym_id']
					select_gym = None
					try:
						select_gym = Gym.objects.get(id=gym_id)
					except:
						return render(request, 'role_panel/select-gym-new-class.html', context={
							'error': True,
							'message': 'لطفا سالن را به درستی انتخاب کنید.'
						})
					return redirect('Main:add_hour', select_gym.id)
				gyms = Gym.objects.filter(area_id__city_id__name=user_logged_in.city)
				coaches = Coach_Profile.objects.all()
				categories = Category.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
				}
				return render(request, 'role_panel/select-gym-new-class.html', context)

			elif role.name == 'superuser':
				if request.method == 'POST' and 'gym_id' in request.POST:
					gym_id = request.POST['gym_id']
					select_gym = None
					try:
						select_gym = Gym.objects.get(id=gym_id)
					except:
						return render(request, 'role_panel/select-gym-new-class.html', context={
							'roles_user_count': roles_user_count,
							'roles_user': roles_user,
							'error': True,
							'message': 'لطفا سالن را به درستی انتخاب کنید.'
						})
					return redirect('Main:add_hour', select_gym.id)

				gyms = Gym.objects.all()
				coaches = Coach_Profile.objects.all()
				categories = Category.objects.all()

				context = {
					'roles_user_count': roles_user_count,
					'roles_user': roles_user,
					'coaches': coaches,
					'gyms': gyms,
					'categories': categories,
				}
				return render(request, 'role_panel/select-gym-new-class.html', context)

			else:
				return redirect('Main:dashboard')
	else:
		return redirect('Accounts/login/?next=/dashboard/select_gym/')


def Hour_Add(request, slug):
	if request.user.is_authenticated:
		user_logged_in = MyUser.objects.get(phone_number=request.user)
		roles_user = Role.objects.filter(user_id__exact=user_logged_in)
		roles_user_count = 0
		roles_user_count = roles_user.count()

		for role in roles_user:
			if role.name == 'superuser':
				if request.method == 'POST' and 'save_form' in request.POST:
					open = request.POST['open']
					close = request.POST['close']
					price = request.POST['price']
					day = request.POST['day']
					gym_id = Gym.objects.get(id=slug)

					try:
						hour = Hour.objects.get(gym_id=gym_id, day=day, open=open)
						hour.close = close
						hour.price = price
						hour.save()

					except:
						Hour.objects.create(open=open, close=close, price=price, day=day, gym_id=gym_id)
				if request.method == 'POST' and 'delete_form' in request.POST:
					open = request.POST['open']
					close = request.POST['close']
					price = request.POST['price']
					day = request.POST['day']
					gym_id = Gym.objects.get(id=slug)
					try:
						hour = Hour.objects.get(gym_id=gym_id, day=day, open=open, close=close)
						hour.delete()
					except:
						pass

		select_gym = Gym.objects.get(id=slug)
		hour_day_distinct = Hour.objects.filter(Q(gym_id__id=slug)).distinct('day')

		hours = Hour.objects.filter(Q(gym_id__id=slug))
		hours_open = Hour.objects.filter(Q(gym_id__id=slug)).distinct('open')
		open = Hour.objects.filter(Q(gym_id__id=slug))

		now = datetime.today()
		orders = Order.objects.filter(Q(gym_id__id=slug) & Q(order_date__gte=now.date()))
		start_week = now + timedelta(weeks=4)
		if now.weekday() == 0:  # shanbe
			start_week = start_week - timedelta(days=2)
		elif now.weekday() == 1:  # yekshanbe
			start_week = start_week - timedelta(days=3)
		elif now.weekday() == 2:  # doahanbe
			start_week = start_week - timedelta(days=4)
		elif now.weekday() == 3:  # seshanbe
			start_week = start_week - timedelta(days=5)
		elif now.weekday() == 4:  # charshanbe
			start_week = start_week - timedelta(days=6)
		elif now.weekday() == 5:  # panjshanbe
			start_week = start_week
		elif now.weekday() == 6:  # jome
			start_week = start_week - timedelta(days=1)

		day_of_week = {"shanbe": start_week,
					   "yeshanbe": start_week + timedelta(days=1), "doshanbe": start_week + timedelta(days=2),
					   "seshanbe": start_week + timedelta(days=3), "charshanbe": start_week + timedelta(days=4),
					   "panjshanbe": start_week + timedelta(days=5), "jome": start_week + timedelta(days=6)
					   }

		orders_count = Order.objects.filter(Q(gym_id__slug=slug) & Q(order_date__gte=now.date())).count()

		# shanbe
		shanbe = {}

		# yeshanbe
		yeshanbe = {}

		# doshanbe
		doshanbe = {}

		# seshanbe
		seshanbe = {}

		# charshanbe
		charshanbe = {}

		# panjshanbe
		panjshanbe = {}

		# jome
		jome = {}

		condition = {}

		for x in hours_open:
			shanbe[x.id] = True
			yeshanbe[x.id] = True
			doshanbe[x.id] = True
			seshanbe[x.id] = True
			charshanbe[x.id] = True
			panjshanbe[x.id] = True
			jome[x.id] = True

		shanbe_t = {}
		for x in hours_open:
			shanbe_t[x.id] = True
			for hour in hours:
				for key, value in shanbe.items():
					if key == x.id and value == True and hour.day == 'shanbe' and hour.open == x.open:
						shanbe_t[x.id] = False

		yeshanbe_t = {}
		for x in hours_open:
			yeshanbe_t[x.id] = True
			for hour in hours:
				for key, value in yeshanbe.items():
					if key == x.id and value == True and hour.day == 'yeshanbe' and hour.open == x.open:
						yeshanbe_t[x.id] = False

		doshanbe_t = {}
		for x in hours_open:
			doshanbe_t[x.id] = True
			for hour in hours:
				for key, value in doshanbe.items():
					if key == x.id and value == True and hour.day == 'doshanbe' and hour.open == x.open:
						doshanbe_t[x.id] = False

		seshanbe_t = {}
		for x in hours_open:
			seshanbe_t[x.id] = True
			for hour in hours:
				for key, value in seshanbe.items():
					if key == x.id and value == True and hour.day == 'seshanbe' and hour.open == x.open:
						seshanbe_t[x.id] = False

		charshanbe_t = {}
		for x in hours_open:
			charshanbe_t[x.id] = True
			for hour in hours:
				for key, value in charshanbe.items():
					if key == x.id and value == True and hour.day == 'charshanbe' and hour.open == x.open:
						charshanbe_t[x.id] = False

		panjshanbe_t = {}
		for x in hours_open:
			panjshanbe_t[x.id] = True
			for hour in hours:
				for key, value in panjshanbe.items():
					if key == x.id and value == True and hour.day == 'panjshanbe' and hour.open == x.open:
						panjshanbe_t[x.id] = False

		jome_t = {}
		for x in hours_open:
			jome_t[x.id] = True
			for hour in hours:
				for key, value in jome.items():
					if key == x.id and value == True and hour.day == 'jome' and hour.open == x.open:
						jome_t[x.id] = False

		context = {
			'roles_user_count': roles_user_count,
			'roles_user': roles_user,
			'day_of_week': day_of_week,
			'now': now,
			'select_gym': select_gym,
			'hours_open': hours_open,
			'hours': hours,
			'orders_count': orders_count,
			'orders': orders,
			'shanbe': shanbe,
			'shanbe_t': shanbe_t,
			'yeshanbe': yeshanbe,
			'yeshanbe_t': yeshanbe_t,
			'doshanbe': doshanbe,
			'doshanbe_t': doshanbe_t,
			'seshanbe': seshanbe,
			'seshanbe_t': seshanbe_t,
			'charshanbe': charshanbe,
			'charshanbe_t': charshanbe_t,
			'panjshanbe': panjshanbe,
			'panjshanbe_t': panjshanbe_t,
			'jome': jome,
			'jome_t': jome_t,
			'start_week': start_week,

		}

		return render(request, 'role_panel/hour_add.html', context)


def Ghavanin(request):
	return render(request, 'ghavanin.html', context={})
