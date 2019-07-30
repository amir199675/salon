from django.http import HttpResponse
from django.shortcuts import redirect ,render
from zeep import Client
from main.models import *
from Account.models import MyUser
from datetime import datetime
from main.models import Gym


MERCHANT = '3ee469e4-cb8d-11e8-8e1b-000c295eb8fc'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "کد تخفیفی اعمال نشده است"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/dashboard/' # Important: need to edit for realy server.

def send_request(request):
    if request.method == 'POST':
        discount_code = request.POST['discount_code']
        amount = request.POST['paidmoney']
        mobile = request.user
        s_day = request.POST['day']
        s_status = request.POST['status']
        s_description = request.POST['description']
        s_myuser_id = request.POST['myuserid']
        s_gym_id = request.POST['gymid']
        s_hour_id = request.POST['hourid']
        s_order_date = request.POST['orderdate']
        s_total_price = request.POST['totalprice']
        s_select_gym = request.POST['select_gym']
        select_gym = Gym.objects.get(slug=s_select_gym)
        description = "کد تخفیفی اعمال نشده است"  # Required
        user_logged = MyUser.objects.get(phone_number=request.user)
        gym = Gym.objects.get(id=s_gym_id)
        coupon = ''
        if discount_code != '':
            coupon= Coupon.objects.get(code__exact=discount_code)

            if coupon :
                # if coupon.minimum_amount <= int(amount):
                if coupon.group_id:
                    groups_in_coupon = coupon.group_id.all()
                    gyms_in_coupon = coupon.gym_id.all()
                    for gym in gyms_in_coupon:
                        if gym.slug == select_gym.slug:
                            for group in groups_in_coupon:
                                users_in_group = group.user_id.all()
                                for user in users_in_group:
                                    if user == user_logged:
                                        amount = int(amount) - int(coupon.amount)
                                        description = "کد تخفیف شما اعمال گردید"
        slug = gym.slug
        CallbackURL = 'http://127.0.0.1:8000/verify'

        s_order_date = s_order_date.replace(',', '')
        s_order_date = s_order_date.replace('.', '')

        try:
            order_date = datetime.strptime(s_order_date, '%B %d %Y')
        except:
            order_date = datetime.strptime(s_order_date, '%b %d %Y')
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        if result.Status == 100:
            try:
                order = Order.objects.create(order_date=order_date,
                                             gym_id=Gym.objects.get(id=s_gym_id),
                                             myuser_id=MyUser.objects.get(phone_number=request.user),
                                             hour_id=Hour.objects.get(id=s_hour_id),
                                             total_price=s_total_price,
                                             paid_money=amount,
                                             status='Reserving')
                global order_id
                order_id = order.id

            except:
                return HttpResponse('این سانس توسط کاربر دیگری درحال رزرو است... لطفا بعدا امتحان کنید!')


            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:

            return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        order = Order.objects.get(id=order_id)
        order.status = 'Reserved'
        order.save()
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        # return redirect('Main:reservation' ,  order.gym_id.slug)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:

            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        order = Order.objects.get(id=order_id)
        order.delete()

        return render(request,'transmition/faild.html',context={'slug':order.gym_id.slug})

