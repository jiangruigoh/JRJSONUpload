from django.shortcuts import render

# Create your views here.
from .models import Department

# Create your views here.
from rest_framework import viewsets
from .serializers import DepartmentSerializer
from rest_framework import filters
import django_filters.rest_framework


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class DepartmentViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated, )
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Department.objects.all().order_by('code','description','created_at','created_by','updated_at','updated_by')
    serializer_class = DepartmentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['code','description','created_at','created_by','updated_at','updated_by'] 
    search_fields = ['code','description','created_at','created_by','updated_at','updated_by']