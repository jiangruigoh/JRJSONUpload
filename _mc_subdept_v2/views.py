from django.shortcuts import render

# Create your views here.
from .models import Subdept

# Create your views here.
from rest_framework import viewsets
from .serializers import SubdeptSerializer
from rest_framework import filters
import django_filters.rest_framework


class SubdeptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Subdept.objects.all().order_by('mcode','code','description')
    serializer_class = SubdeptSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['mcode','code','description'] 
    search_fields = ['mcode','code','description']