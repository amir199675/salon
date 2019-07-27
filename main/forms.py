from django import forms
from .models import *

class TicketForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-align: right', 'id': 'fname', 'class': 'form-control','name':'name' }))

    family_name = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-align: right', 'id': 'lname', 'class': 'form-control','name':'family_name' }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'style': 'text-align: right', 'id': 'email', 'class': 'form-control','name':'email' }))

    title = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'text-align: right', 'id': 'subject', 'class': 'form-control', 'name': 'title'}))

    text = forms.CharField(widget=forms.Textarea(
        attrs={'style': 'text-align: right', 'id': 'message', 'class': 'form-control',
               'placeholder': 'لطفا متن پیام خود را وارد کنید', 'name': 'text'}))

    class Meta:
        model = Ticket
        fields = ('name','family_name','email','title','text')


#
# class CoachProfileForm(forms.ModelForm):
#
#
#
#     class Meta: