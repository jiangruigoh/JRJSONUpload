from django.shortcuts import render

# Create your views here.
from .models import Supcus

# Create your views here.
from rest_framework import viewsets
from .serializers import SupcusSerializer
from rest_framework import filters
import django_filters.rest_framework


class SupcusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Supcus.objects.all().order_by('code','name','supcus_guid')
    serializer_class = SupcusSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['code','name','supcus_guid'] 
    search_fields = ['code','name','supcus_guid']		