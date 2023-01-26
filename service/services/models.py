from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_delete

from clients.models import Client
from .tasks import set_price, set_comment
from .signals import delete_cache_total_sum

class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return 'service  - {0}'.format(self.name)

    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price   

    def save(self, *args,  **kwargs):
        super().save(*args, **kwargs)
        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return super().save(*args, **kwargs)

class Plan(models.Model):
    PLAN_TYPES = (
        ('full','Full'),
        ('student','Student'),
        ('discount','Discount'),
    )

    plan_type = models.CharField(choices = PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0,
                                                    validators=[
                                                        MaxValueValidator(100)
                                                    ])
    
    def __str__(self) -> str:
        return 'plan - {0}'.format(self.plan_type)

    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent   

    def save(self, *args,  **kwargs):
        super().save(*args, **kwargs)
        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return super().save(*args, **kwargs)

class Subscription(models.Model):
    client =  models.ForeignKey(Client, on_delete = models.PROTECT, related_name = 'subscriptions')
    service =  models.ForeignKey(Service, on_delete = models.PROTECT, related_name = 'subscriptions')
    plan =  models.ForeignKey(Plan, on_delete = models.PROTECT, related_name = 'subscriptions')
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default='')

    def __str__(self) -> str:
        return '{0}, {1}, {2}'.format(self.client, self.service, self.plan)

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result =  super().save(*args, **kwargs)
        if creating:
            set_price.delay(self.id)
        return result

post_delete.connect(delete_cache_total_sum, sender = Subscription)