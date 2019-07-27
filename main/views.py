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
    def post(self, request,format=None):
        serializers = ProvincesSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)





class APIListCreateCity(APIView):
    def get(self, request, format=None):
        cites = City.objects.all()
        serializer = CitiesSerializers(cites, many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializers = CitiesSerializers(data=request.data)
        id = request.data['province_id']
        province_id = Province.objects.get(id=id)
        serializers.is_valid(raise_exception=True)
        City.objects.create(name=request.data['name'],province_id=province_id)
        return Response(serializers.data,status=status.HTTP_201_CREATED)


class APIListArea(APIView):
    def get(self, request, format=None):
        areas = Area.objects.all()
        serializer = AreasSerializers(areas, many=True)
        return Response(serializer.data)





def Index(request):
    if request.method == 'POST' and 'favorite' in request.POST:
        user = request.user
        fav = request.POST['fav']
        try:
            favorite = Favourite.objects.get(myuser_id=MyUser.objects.get(phone_number = user),gym_id=Gym.objects.get(id = fav))
            favorite.delete()
            return redirect('Main:index')
        except:
            favorite = Favourite.objects.create(myuser_id=MyUser.objects.get(phone_number = user),gym_id=Gym.objects.get(id = fav))
            favorite.save()
            return redirect('Main:index')

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

        favorites = Favourite.objects.filter(gym_id__area_id__city_id__name=user_city,myuser_id__phone_number=user_phone_number)

        if favorites:
            pass
        else:
            favorites = {'Amir:D':'Amir:D'}
        gyms = Gym.objects.filter(area_id__city_id__name=user_city)  # salon haye dar ostan user login karde

        counter_comments = {}

        categories = Category.objects.all()

        # dar inja ba dictionary esm province city va area ro gereftam
        province_gym = {}
        area_gym = {}
        city_gym = {}
        gym_search_area = Area.objects.all().distinct('name')
        gym_search_province = Province.objects.all().distinct('name')
        gym_search_city = City.objects.all().distinct('name')

        for area in gym_search_area:
            area_gym[area.name] = area.name

        for city in gym_search_city:
            city_gym[city.name] = city.name

        for province in gym_search_province:
            province_gym[province.name] = province.name

        for gym in gyms:
            counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

        context = {'user_logged': user_logged,
                   'gyms': gyms,
                   'name': name,
                   'counter_comments': counter_comments,
                   'area_gym': area_gym,
                   'province_gym': province_gym,
                   'city_gym': city_gym,
                   'categories': categories,
                   'favorites':favorites,
                   'bascketbal':bascketbal,
                   'footbal':footbal,
                   'footsal':footsal,
                   'tenis':tenis,
                   'volybal':volybal,
                   'gyms_count':gyms_count,
                   }
        return render(request, 'index.html', context)










    elif request.user.is_authenticated == False:

        counter_comments = {}

        province_gym = {}
        area_gym = {}
        city_gym = {}
        gym_search_area = Area.objects.all().distinct('name')
        gym_search_province = Province.objects.all().distinct('name')
        gym_search_city = City.objects.all().distinct('name')

        for area in gym_search_area:
            area_gym[area.name] = area.name

        for city in gym_search_city:
            city_gym[city.name] = city.name

        for province in gym_search_province:
            province_gym[province.name] = province.name

        gyms = Gym.objects.all()
        categories = Category.objects.all()

        for gym in gyms:
            counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

        context = {
            'area_gym': area_gym,
            'province_gym': province_gym,
            'city_gym': city_gym,
            'gyms': gyms,
            'counter_comments': counter_comments,
            'categories': categories,

        }
        return render(request, 'index.html', context)


def Gym_List(request):
    if request.method == 'GET' and 'search_gym' in request.GET:
        province = request.GET.get('province', 'not found')
        city = request.GET.get('city', 'not found')
        area = request.GET.get('area', 'not found')
        category = request.GET.get('province', 'not found')
        sex = request.GET.get('sex', 'not found')

        gyms = Gym.objects.filter(area_id__name=area, area_id__city_id__name=city,
                                  area_id__city_id__province_id__name=province)

        context = {

        }

        return render(request, 'gym_list.html', context)

    counter_comments = {}

    categories = Category.objects.all()

    # dar inja ba dictionary esm province city va area ro gereftam
    province_gym = {}
    area_gym = {}
    city_gym = {}
    gym_search_area = Area.objects.all().distinct('name')
    gym_search_province = Province.objects.all().distinct('name')
    gym_search_city = City.objects.all().distinct('name')

    for area in gym_search_area:
        area_gym[area.name] = area.name

    for city in gym_search_city:
        city_gym[city.name] = city.name

    for province in gym_search_province:
        province_gym[province.name] = province.name

    gyms = Gym.objects.all()
    paginator = Paginator(gyms, 10)
    page = request.GET.get('page')
    gyms_list = paginator.get_page(page)

    for gym in gyms:
        counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

    context = {

        'counter_comments': counter_comments,
        'area_gym': area_gym,
        'province_gym': province_gym,
        'city_gym': city_gym,
        'categories': categories,
        'gyms': gyms_list
    }

    return render(request, 'gym_list.html', context)


def Gym_Single(request, slug):
    select_gym = Gym.objects.get(slug=slug)
    gyms = Gym.objects.filter(area_id__city_id__province_id__name=select_gym.area_id.city_id.province_id)
    facilities = Gym_Facility.objects.all()
    just_faci = Facility.objects.all()

    counter_comments = {}
    for gym in gyms:
        counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

    context = {
        'gyms': gyms,
        'select_gym': select_gym,
        'counter_comments': counter_comments,
        'facilities': facilities,
        'just_faci': just_faci

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
        'next_key':next_key,
        'back_key':back_key,
        'first_week':first_week,
        'day_of_week':day_of_week,
        'now':now,
        'select_gym':select_gym,
        'hours_open':hours_open,
        'hours':hours,
        'orders_count':orders_count,
        'orders':orders,
        'shanbe_e':shanbe_e,
        'shanbe':shanbe,
        'shanbe_t':shanbe_t,
        'yeshanbe_e':yeshanbe_e,
        'yeshanbe':yeshanbe,
        'yeshanbe_t':yeshanbe_t,
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
        'start_week':start_week,
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


def Accept(request,slug):


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

        s_order_date = s_order_date.replace(',','')
        s_order_date = s_order_date.replace('.', '')

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
            'reserve':True,
            's_day':s_day,
            's_description':s_description,
            's_gym_id':s_gym_id,
            's_hour_id':s_hour_id,
            's_myuser_id':s_myuser_id,
            's_order_date':s_order_date,
            's_paid_money':s_paid_money,
            's_status':s_status,
            's_total_price':s_total_price,

        }


        return render(request,'modal_reserv.html',context)


def Work_Request(request):

    if request.user.is_authenticated:

        user_phone_number = request.user
        user_logged = MyUser.objects.get(phone_number=user_phone_number)
        name = user_logged.name
        if request.method == 'POST':
            name = request.POST['name']
            family = request.POST['family_name']
            email = request.POST['email']
            title = request.POST['title']
            text = request.POST['text']
            tf = TicketForm(request.POST)
            if tf.is_valid():
                worker_req = Ticket.objects.create(name=name,family_name=family,myuser_id=user_logged,email=email,title=title,text=text)
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

    else:
        if request.method == 'POST':
            tf = TicketForm(request.POST)
            if tf.is_valid():
                tf.save()
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


def Coacher_Page(request, slug):
    training_class = Training_Class.objects.get(slug=slug)

    context = {
        'training_class': training_class
    }
    return render(request, 'coachpage.html', context)


def Classes_List(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # area = Training_Class.objects.filter(gym_id__area_id__name=)
            pass

        else:
            user_phone_number = request.user
            user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
            user_province = user_logged_in.province
            counter_comments = {}

            classes = Training_Class.objects.filter(gym_id__area_id__city_id__province_id__name=user_province)
            for clas in classes:
                counter_comments[clas.gym_id.name] = Comment.objects.filter(gym_id__name=clas.gym_id.name).count()

            context = {
                'classes': classes,
                'counter_comments': counter_comments,

            }
            return render(request, 'teaching.html', context)
    else:
        counter_comments = {}
        classes = Training_Class.objects.all()
        for clas in classes:
            counter_comments[clas.gym_id.name] = Comment.objects.filter(gym_id__name=clas.gym_id.name).count()

        context = {
            'classes': classes,
            'counter_comments': counter_comments,

        }
        return render(request, 'teaching.html', context)


def Dashboard(request):
    if request.user.is_authenticated:
        user_phone_number = request.user
        user_logged_in = MyUser.objects.get(phone_number=user_phone_number)
        orders = Order.objects.filter(myuser_id=request.user)
        try:
            user_logged_in_rols = Role_MyUser.objects.get(myuser_id__phone_number=user_phone_number)
            user_logged_in_rol = user_logged_in_rols.role_id.name
        except Role_MyUser.DoesNotExist:
            user_logged_in_rols = None
            user_logged_in_rol = None

        # admin access
        gyms_counter = Gym.objects.all().count()
        users_counter = MyUser.objects.all().count()
        orders_counter = Order.objects.all().count()
        teachers_counter = Role_MyUser.objects.filter(role_id__name='teacher').count()

        roles = Role.objects.all()
        context = {
            'user_counter': users_counter,
            'roles': roles,
            'user_logged_in': user_logged_in,
            'orders_counter': orders_counter,
            'teachers_counter': teachers_counter,
            'gyms_counter': gyms_counter,
            'user_logged_in_rol': user_logged_in_rol,
            'user_logged_in_rols': user_logged_in_rols,
            'orders':orders,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('Account:login')


def Create_Gym(request):
    context = {}
    return render(request, 'new_gym.html', context)


def Delete_Role_Group(request):
    if request.method == 'POST' and 'delete_form' in request.POST:

        for str in request.POST.getlist('roll'):
            try:
                list_splited = str.split('Amir:D')
                delete_rol = Role.objects.get(user_id=MyUser.objects.get(pk=int(list_splited[1])), name=list_splited[0])
                delete_rol.delete()
            except:
                return redirect('Main:delete_role_group')

        for str in request.POST.getlist('groupp'):
            try:
                list_splited = str.split('Amir:D')
                delete_group = Group.objects.get(user_id=MyUser.objects.get(pk=int(list_splited[1])),
                                                 name=list_splited[0])
                delete_group.delete()
            except:
                return redirect('Main:delete_role_group')

        return redirect('Main:delete_role_group')

    if request.method == 'GET' and 'search_form' in request.GET:
        rol = request.GET['rol']
        group = request.GET['group']
        national_number = request.GET['national_number']
        phone_number = request.GET['phone_number']

        rols = Role.objects.all().distinct('name')
        groups = Group.objects.all().distinct('name')

        users = MyUser.objects.filter(Q(group__name=group) | Q(role__name=rol) | Q(national_number=national_number) | Q(
            phone_number=phone_number))
        return render(request, 'deletuser.html', locals())

    users = MyUser.objects.all()
    rols = Role.objects.all().distinct('name')
    groups = Group.objects.all().distinct('name')

    return render(request, 'deletuser.html', locals())


def Add_Role_Group(request):
    rols = Role.objects.all().distinct('name')
    groups = Group.objects.all().distinct('name')
    users = MyUser.objects.all()
    if request.method == 'POST':
        for group in groups:  # baraye har groh ke entekhab mikone chon name dar template {{ group.name }} tarif shode
            if group.name in request.POST:
                for user in request.POST.getlist('groups'):
                    try:
                        Group.objects.get(user_id=user, name=group.name)
                    except:
                        selected = user
                        add_group = Group.objects.create(name=group.name)
                        add_group.user_id.add(selected)
                        add_group.save()

        return redirect('Main:add_role_group')

    users = MyUser.objects.all()
    rols = Role.objects.all().distinct('name')
    groups = Group.objects.all().distinct('name')

    return render(request, 'alluser.html', locals())


def Edite_Gym_info(request):
    gyms = Gym.objects.all()

    return render(request, 'all_gyms.html', locals())


def Edit_Profile_Teacher(request):
    if request.method == 'POST' and 'save_form' in request.POST:
        name = request.POST['name']
        department_name = request.POST['department_name']
        job = request.POST['job']
        national_number = request.POST['national_number']
        text = request.POST['text']
        phone_number = request.POST['phone_number']

        user_logged_in = MyUser.objects.get(id=request.user.id)
        user_logged_in.national_number = national_number
        user_logged_in.phone_number = phone_number
        user_logged_in.name = name
        user_logged_in.save()

        user_profile = Coach_Profile.objects.get(user_id=request.user)
        user_profile.text = text
        user_profile.job = job
        user_profile.department_name = department_name
        user_profile.save()

        return redirect('Main:edit_profile')

    if request.user:
        coach_profiles = Coach_Profile.objects.all()
        for coach_profile in coach_profiles:
            if coach_profile.user_id == request.user:
                coach = Coach_Profile.objects.get(user_id=request.user)
                return render(request, 'couchprofile.html', locals())
            else:
                return redirect('Main:dashboard')

    return redirect('Account:login')


def Add_Facility(request):
    facilities = Facility.objects.all()
    context = {
        'facilities': facilities
    }
    return render(request, 'add_facility.html', context)



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


def select_category(request,category):
    gyms = Gym.objects.filter(category_id__name=category)

    counter_comments = {}

    categories = Category.objects.all()

    # dar inja ba dictionary esm province city va area ro gereftam
    province_gym = {}
    area_gym = {}
    city_gym = {}
    gym_search_area = Area.objects.all().distinct('name')
    gym_search_province = Province.objects.all().distinct('name')
    gym_search_city = City.objects.all().distinct('name')

    for area in gym_search_area:
        area_gym[area.name] = area.name

    for city in gym_search_city:
        city_gym[city.name] = city.name

    for province in gym_search_province:
        province_gym[province.name] = province.name

    paginator = Paginator(gyms, 10)
    page = request.GET.get('page')
    gyms_list = paginator.get_page(page)

    for gym in gyms:
        counter_comments[gym.name] = Comment.objects.filter(gym_id__name=gym.name).count()

    context = {

        'counter_comments': counter_comments,
        'area_gym': area_gym,
        'province_gym': province_gym,
        'city_gym': city_gym,
        'categories': categories,
        'gyms': gyms_list,
        'category':category
    }

    return render(request, 'list_by_type.html', context)




