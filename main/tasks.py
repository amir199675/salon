from datetime import datetime, timedelta
from .models import Order
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=10)
def delete_expire():
    orders = Order.objects.filter(status='Reserving')

    for order in orders:
        if order.created + timedelta(minutes=9) < datetime.now():
            order.delete()
            print('done!')


register_events(scheduler)