from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from clients.models import Client
from .serializers import SubscriptionSerializer
from django.db.models import Prefetch



class SubscriptionView(ReadOnlyModelViewSet):


    queryset = Subscription.objects.prefetch_related(
        'plan',
        Prefetch(
            'client',queryset = Client.objects.select_related('user').only(
                'company_name',
                'user__email'
            )
        )
    )
    serializer_class = SubscriptionSerializer

