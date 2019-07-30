from django import forms
import random
from .models import *
from main.models import Ticket
from django.contrib.auth.hashers import make_password
import string



class MyUserForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'padding-right: 50px', 'class': 'class1 input100', 'placeholder': '      نام و نام خانوادگی',
               'data-msg': 'Please enter at least 4 chars', 'name': 'name', }))

    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'padding-right: 50px', 'class': 'class1 input100', 'placeholder': '      شماره تلفن همراه',
               'data-msg': 'Please enter at least 4 chars', 'name': 'mobile', }))

    national_number = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'padding-right: 50px', 'class': 'class1 input100', 'placeholder': '      کد ملی',
               'data-msg': 'Please enter at least 4 chars', 'name': 'national_number', }))

    province = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'class1 input100', 'placeholder': '      استان', 'list': 'browserr',
               'data-msg': 'Please enter at least 4 chars', 'name': 'province', }))

    city = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'class1 input100', 'placeholder': '      شهر', 'list': 'browser',
               'data-msg': 'Please enter at least 4 chars', 'name': 'city', }))

    area = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'class1 input100', 'placeholder': '      منطقه', 'list': 'browsers',
               'data-msg': 'Please enter at least 4 chars', 'name': 'area', }))

    activation_code = forms.CharField(required=False,widget=forms.HiddenInput())


    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'style': 'padding-right: 50px','type':'password', 'class': 'class1 input100', 'placeholder': '      رمز عبور',
               'name': 'password'}))

    re_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'style': 'padding-right: 50px','type':'password', 'class': 'class1 input100', 'placeholder': '      تکرار رمز عبور',
               'name': 're_password'}))


    class Meta:
        model = MyUser
        fields = ('name', 'phone_number', 'national_number', 'province', 'city', 'area', 'password', 're_password','activation_code')
