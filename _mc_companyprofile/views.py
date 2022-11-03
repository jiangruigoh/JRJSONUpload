from django.shortcuts import render

# Create your views here.
from .models import Companyprofile

# Create your views here.
from rest_framework import viewsets
from .serializers import CompanyprofileSerializer
from rest_framework import filters
import django_filters.rest_framework


class CompanyprofileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Companyprofile.objects.all().order_by('locgroup_branch')
    serializer_class = CompanyprofileSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['locgroup_branch','companyname'] 
    search_fields = ['locgroup_branch']	