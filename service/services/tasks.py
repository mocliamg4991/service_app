import time
from celery import shared_task
from django.db.models import F
import datetime
from django.db import transaction

@shared_task
def set_price(subscription_id):

    from services.models import Subscription    
    with transaction.atomic():



        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(annotated_price=F('service__full_price') -
                                                                                F('service__full_price') * (F('plan__discount_percent')/100.00)).first()


        subscription.price = subscription.annotated_price
        subscription.save()
    print('do_something')

@shared_task
def set_comment(subscription_id):

    from services.models import Subscription  
    print('do_something')
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)


        subscription.comment = str(datetime.datetime.now())
        subscription.save()
    print('do_something')