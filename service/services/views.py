from django.db.models import Prefetch
from django.db.models import F, Sum
from django.core.cache import cache
from .serializers import SubscriptionSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription
from clients.models import Client
from django.conf import settings

class SubscriptionView(ReadOnlyModelViewSet):


    queryset = Subscription.objects.prefetch_related(
        'plan',
        Prefetch(
            'client',
            queryset = Client.objects.select_related('user').only(
                'company_name',
                'user__email'
            )
        )
    )
    
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else: 
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60*60)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data
        return response
