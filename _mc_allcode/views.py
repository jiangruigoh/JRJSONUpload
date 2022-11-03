from django.shortcuts import render

# Create your views here.
from .models import Allcode

# Create your views here.
from rest_framework import viewsets
from .serializers import AllcodeSerializer
from rest_framework import filters
import django_filters.rest_framework


class AllcodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Allcode.objects.all().order_by('code','description')
    serializer_class = AllcodeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['code','description'] 
    search_fields = ['code','description']