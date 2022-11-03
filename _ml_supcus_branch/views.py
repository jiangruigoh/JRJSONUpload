from django.shortcuts import render

# Create your views here.
from .models import SupcusBranch

# Create your views here.
from rest_framework import viewsets
from .serializers import SupcusBranchSerializer
from rest_framework import filters
import django_filters.rest_framework


class SupcusBranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SupcusBranch.objects.all().order_by('supcus_guid','loc_group','set_active')
    serializer_class = SupcusBranchSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['supcus_guid','loc_group','set_active'] 
    search_fields = ['supcus_guid','loc_group','set_active']	