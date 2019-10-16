from django.http import HttpResponse
from django.shortcuts import redirect ,render ,reverse
from zeep import Client
from main.models import *
from Account.models import MyUser
from datetime import datetime
from main.models import Gym , Training_Class
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

MERCHANT = 'pyB7u84G0DD6G15Vkm45'
client = Client('https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx?wsdl')
amount = 1000  # Toman / Required
description = "کد تخفیفی اعمال نشده است"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional





def send_reques(method, data):
    ws_method = getattr(client.service, method)
    result = ws_method(data)
    return result

import random

def RandForOrderId():
    while(True):
        number = random.randint(100000,999999)
        return number


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

        s_order_date = s_order_date.replace(',', '')
        s_order_date = s_order_date.replace('.', '')
        try:
            order_date = datetime.strptime(s_order_date, '%B %d %Y')
        except:
            order_date = datetime.strptime(s_order_date, '%b %d %Y')
        callback_url = str(request.build_absolute_uri('/verify/'))
        # return HttpResponse(callback_url)
        request_data = {
            'LoginAccount': MERCHANT,
            'OrderId': RandForOrderId(),
            'Amount': amount,
            'CallBackUrl': 'https://salon-yab.ir/verify/'
        }

        result = client.service.SalePaymentRequest(request_data)
        while(result.Status == -112):
            request_data = {
                'LoginAccount': MERCHANT,
                'OrderId': RandForOrderId(),
                'Amount': amount,
                'CallBackUrl': callback_url
            }
            result = client.service.SalePaymentRequest(request_data)
        # return HttpResponse(result)
        if result.Status == 0:
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


            return redirect('https://pec.shaparak.ir/NewIPG/?token='+str(result.Token))
        else:

            return HttpResponse('Error code: ' + str(result.Status))


@csrf_exempt
def verify(request):
    if int(request.POST.get('status'))== 0 and int(request.POST.get('RRN')) > 0 :
        order = Order.objects.get(id=order_id)
        order.status = 'Reserved'
        order.save()

    else:
        order = Order.objects.get(id=order_id)
        order.delete()
        return render(request,'transmition/faild.html',context={'slug':order.gym_id.slug})

def request_class(request):
    if request.method == 'POST':
        select_training = request.POST['select_training']
        user = request.POST['user']
        global select_user
        select_user = MyUser.objects.get(id=user)
        select_training = Training_Class.objects.get(id=select_training)
        global select_training_id
        select_training_id = select_training.id
        amount = select_training.price

        result = client.service.SalePaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        if result.Status == 100:

            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))


def verify_class(request):
    training = Training_Class.objects.get(id=select_training_id)


    if request.GET.get('Status') == 'OK':
        training = Training_Class.objects.get(id=select_training_id)
        training.user_id.add(select_user)
        training.save()
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        # return redirect('Main:reservation' ,  order.gym_id.slug)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:

            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return render(request, 'transmition/faild.html', context={'slug': training.slug,
                                                                  'amir': True})
