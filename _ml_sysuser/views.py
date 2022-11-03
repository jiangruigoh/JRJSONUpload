from django.shortcuts import render

# Create your views here.
from .models import Sysuser

# Create your views here.
from rest_framework import viewsets
from .serializers import SysuserSerializer
from rest_framework import filters
import django_filters.rest_framework


class SysuserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sysuser.objects.all().order_by('name')
    serializer_class = SysuserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['name','fullname'] 
    search_fields = ['name']	