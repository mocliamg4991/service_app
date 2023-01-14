from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ClientSerializer
from .models import Client
from django.db.models import Prefetch
from django.contrib.auth.models import User

class ClientView(ReadOnlyModelViewSet):
    queryset = Client.objects.prefetch_related(
        Prefetch(
            'user', queryset= User.objects.only('first_name','last_name','email')
        )
    )
    serializer_class = ClientSerializer

