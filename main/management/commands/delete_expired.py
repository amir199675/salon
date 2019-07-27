# from django.core.management.base import BaseCommand
# from datetime import timedelta , datetime
# from main.models import Order
# import datetime
# import pytz
#
# utc=pytz.UTC
#
#
#
# class Command(BaseCommand):
#     help = 'Deletes expired rows'
#
#     def handle(self, *args, **options):
#
#
#         orders = Order.objects.filter(status='Reserving')
#
#         for order in orders:
#             condition = (order.created + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
#             condition1 = datetime.datetime.strptime(condition ,"%Y-%m-%d %H:%M:%S")
#             condition2 = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
#             print(condition1)
#             print(condition2)
#             # if condition1 <= condition2:
#             #     amir = order
#             #     amir.delete()
#             #     print('hello')