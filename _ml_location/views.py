from django.shortcuts import render

# Create your views here.
from .models import Location

# Create your views here.
from rest_framework import viewsets
from .serializers import LocationSerializer
from rest_framework import filters
import django_filters.rest_framework


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Location.objects.all().order_by('locgroup','code','description')
    serializer_class = LocationSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['locgroup','code','description'] 
    search_fields = ['locgroup','code','description']	