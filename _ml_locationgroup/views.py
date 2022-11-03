from django.shortcuts import render

# Create your views here.
from .models import Locationgroup

# Create your views here.
from rest_framework import viewsets
from .serializers import LocationgroupSerializer
from rest_framework import filters
import django_filters.rest_framework


class LocationgroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Locationgroup.objects.all().order_by('code','description')
    serializer_class = LocationgroupSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['code','description'] 
    search_fields = ['code','description']												