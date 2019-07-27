from django.shortcuts import render, reverse, redirect

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .forms import MyUserForm
from django.contrib.auth import authenticate, login, logout
from main.models import *
from django.http import HttpResponse
from django.http import JsonResponse
import random
import requests
import json


def random_string_mobile():
    code = random.randrange(start=10000, stop=99999, step=1)
    return code


# Create your views here.
def Login(request):

    if request.method == 'POST' and 'register_form' in request.POST:

        uf = MyUserForm(request.POST)
        password = request.POST['password']
        re_password = request.POST['re_password']
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        national_number = request.POST['national_number']
        province = request.POST['province']
        city = request.POST['city']
        area = request.POST['area']
        request.session['phone_number'] = phone_number
        provinces = Province.objects.all()
        try:
            myuser = MyUser.objects.get(
                Q(phone_number=phone_number) & Q(national_number=national_number) & Q(is_code_active=False) | Q(
                    phone_number=phone_number) & Q(national_number=national_number) & Q(is_code_active=True))
            exist = True
        except:
            exist = False

        try:
            myuser = MyUser.objects.get(Q(phone_number=phone_number) | Q(national_number=national_number))
            other = True
        except:
            other = False
        try:
            myuser = MyUser.objects.get(
                Q(phone_number=phone_number) & Q(national_number=national_number) & Q(is_code_active=False))
            activation_code_status = True
        except:
            activation_code_status = False

        if password == re_password:
            if uf.is_valid():
                if exist:

                    if activation_code_status:
                        myuser = MyUser.objects.get(phone_number=phone_number)
                        data = {'UserApiKey': '578cdf057764feb86880e3d2', 'SecretKey': '13491375amirelyas'}
                        r = requests.post('https://RestFulSms.com/api/Token', data=data)  # get TokenApi
                        amir = json.loads(r.text)
                        amir = amir['TokenKey']
                        headers = {'x-sms-ir-secure-token': amir}
                        data = {'code': myuser.activation_code, 'MobileNumber': myuser.phone_number}
                        r = requests.post(url='https://RestFulSms.com/api/VerificationCode', headers=headers,
                                          data=data)
                        context = {

                        }
                        return render(request, '', context)
                    else:  # user fa'al ast
                        context = {}
                        return render(request, '', context)
                elif other:  # information of other user
                    context = {}
                    return render(request, '', context)

                user = MyUser.objects.create(name=name, phone_number=phone_number, national_number=national_number,
                                             province=province, city=city, area=area,
                                             activation_code=random_string_mobile())
                user.set_password(password)
                user.save()
                uf = MyUserForm()
                context = {
                    'uf': uf,
                    'provinces': provinces,
                    'signup': True,
                    'modal': True
                }
                data = {'UserApiKey': '578cdf057764feb86880e3d2', 'SecretKey': '13491375amirelyas'}
                r = requests.post('https://RestFulSms.com/api/Token', data=data)  # get TokenApi
                amir = json.loads(r.text)
                amir = amir['TokenKey']
                headers = {'x-sms-ir-secure-token': amir}
                data = {'code': user.activation_code, 'MobileNumber': user.phone_number}
                r = requests.post(url='https://RestFulSms.com/api/VerificationCode', headers=headers,
                                  data=data)
                return render(request, 'register/index.html', context)

        else:
            message = 'پسورد را به درستی وارد کنید'
            context = {
                'uf': uf,
                'signup': True,
                'provinces': provinces,
                'message': message,
                'error': True
            }
            return render(request, 'register/index.html', context)
    if request.method == 'POST' and 'modal_form' in request.POST:
        user = MyUser.objects.get(phone_number=request.session['phone_number'])
        activation_code = request.POST['code']
        if user.activation_code == activation_code:
            user.activation_code = random_string_mobile()
            user.is_code_active = True
            user.save()
            return redirect('Account:login')
        else:
            context = {
                'message': 'کد شما صحیح نمیباشد.',
                'error': True,
                'modal': True,
                'signup': True
            }
            return render(request, 'register/index.html', context)


    if request.method == 'POST' and 'login_form' in request.POST:
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(username=phone_number, password=password)

        if user is not None:
            if user.is_active and user.is_code_active:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                request.session['user_phone_number'] = phone_number
                return redirect('Main:index')
            else:
                message = 'کد فعال سازی را دوباره درخواست نمایید'
                context = {
                    'login': True,
                    'message':message,
                    'error':True
                }
                return render(request, 'register/index.html', context)
        else:

            uf = MyUserForm()
            provinces = Province.objects.all()
            cities = City.objects.all()
            areas = Area.objects.values('name').distinct()

            context = {
                'uf': uf,
                'provinces': provinces,
                'cities': cities,
                'areas': areas,
                'message': 'مشخصات خود را به طور صحیح وارد کنید.',
                'error': True
            }
            return render(request, 'register/index.html', context)

    if request.method == 'POST' and 'date' in request.POST:
        uf = MyUserForm()
        provinces = Province.objects.all()
        cities = City.objects.all()
        areas = Area.objects.values('name').distinct()
        context = {
            'uf': uf,
            'provinces': provinces,
            'cities': cities,
            'areas': areas,
            'error':True,
            'message':'برای رزرو سالن حتما باید به حساب خود وارد شوید.'

        }
        return render(request, 'register/index.html', context)


    else:
        uf = MyUserForm()
        provinces = Province.objects.all()
        cities = City.objects.all()
        areas = Area.objects.values('name').distinct()
        context = {
            'uf': uf,
            'provinces': provinces,
            'cities': cities,
            'areas': areas,

        }
        return render(request, 'register/index.html', context)


def Register(request):

    if request.method == 'POST' and 'login_form' in request.POST:
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(username=phone_number, password=password)

        if user is not None:
            if user.is_active and user.is_code_active:
                login(request, user)
                request.session['user_phone_number'] = phone_number
                return redirect('Main:index')
            else:
                context = {
                    'login': True,

                }
                return render(request, 'register/index.html', context)

        else:

            uf = MyUserForm()
            provinces = Province.objects.all()
            cities = City.objects.all()
            areas = Area.objects.values('name').distinct()

            context = {
                'uf': uf,
                'provinces': provinces,
                'cities': cities,
                'areas': areas,
                'message': 'مشخصات خود را به طور صحیح وارد کنید.',
                'error': True
            }
            return render(request, 'register/index.html', context)

    if request.method == 'POST' and 'register_form' in request.POST:

        uf = MyUserForm(request.POST)
        password = request.POST['password']
        re_password = request.POST['re_password']
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        national_number = request.POST['national_number']
        province = request.POST['province']
        city = request.POST['city']
        area = request.POST['area']
        request.session['phone_number'] = phone_number
        provinces = Province.objects.all()
        try:
            myuser = MyUser.objects.get(
                Q(phone_number=phone_number) & Q(national_number=national_number) & Q(is_code_active=False) | Q(
                    phone_number=phone_number) & Q(national_number=national_number) & Q(is_code_active=True))
            exist = True
        except:
            exist = False

        try:
            myuser = MyUser.objects.get(Q(phone_number=phone_number) | Q(national_number=national_number))
            other = True
        except:
            other = False
        try:
            myuser = MyUser.objects.get(
                Q(phone_number=phone_number) & Q(national_number=national_number) & Q(is_code_active=False))
            activation_code_status = True
        except:
            activation_code_status = False

        if password == re_password:
            if uf.is_valid():
                if exist:

                    if activation_code_status:
                        myuser = MyUser.objects.get(phone_number=phone_number)
                        data = {'UserApiKey': '578cdf057764feb86880e3d2', 'SecretKey': '13491375amirelyas'}
                        r = requests.post('https://RestFulSms.com/api/Token', data=data)  # get TokenApi
                        amir = json.loads(r.text)
                        amir = amir['TokenKey']
                        headers = {'x-sms-ir-secure-token': amir}
                        data = {'code': myuser.activation_code, 'MobileNumber': myuser.phone_number}
                        r = requests.post(url='https://RestFulSms.com/api/VerificationCode', headers=headers,
                                          data=data)
                        context = {

                        }
                        return render(request, '', context)
                    else:  # user fa'al ast
                        context = {}
                        return render(request, '', context)
                elif other:  # information of other user
                    context = {}
                    return render(request, '', context)

                user = MyUser.objects.create(name=name, phone_number=phone_number, national_number=national_number,
                                             province=province, city=city, area=area,
                                             activation_code=random_string_mobile())
                user.set_password(password)
                user.save()
                uf = MyUserForm()
                context = {
                    'uf': uf,
                    'provinces': provinces,
                    'signup': True,
                    'modal': True
                }
                data = {'UserApiKey': '578cdf057764feb86880e3d2', 'SecretKey': '13491375amirelyas'}
                r = requests.post('https://RestFulSms.com/api/Token', data=data)  # get TokenApi
                amir = json.loads(r.text)
                amir = amir['TokenKey']
                headers = {'x-sms-ir-secure-token': amir}
                data = {'code': user.activation_code, 'MobileNumber': user.phone_number}
                r = requests.post(url='https://RestFulSms.com/api/VerificationCode', headers=headers,
                                  data=data)
                return render(request, 'register/index.html', context)

        else:
            message = 'پسورد را به درستی وارد کنید'
            context = {
                'uf': uf,
                'signup': True,
                'provinces': provinces,
                'message': message,
                'error': True
            }
            return render(request, 'register/index.html', context)
    if request.method == 'POST' and 'modal_form' in request.POST:
        user = MyUser.objects.get(phone_number=request.session['phone_number'])
        activation_code = request.POST['code']
        if user.activation_code == activation_code:
            user.activation_code = random_string_mobile()
            user.is_code_active = True
            user.save()
            return redirect('Account:login')
        else:
            context = {
                'message': 'کد شما صحیح نمیباشد.',
                'error': True,
                'modal': True,
                'signup': True
            }
            return render(request, 'register/index.html', context)
    else:
        uf = MyUserForm()
        provinces = Province.objects.all()
        cities = City.objects.all()
        areas = Area.objects.values('name').distinct()
        context = {
            'uf': uf,
            'signup': True,
            'provinces': provinces,
            'cities': cities,
            'areas': areas,
        }
        return render(request, 'register/index.html', context)


def LogOut(request):
    logout(request)
    return redirect('Main:index')
