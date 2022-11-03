from django.shortcuts import render

# Create your views here.
from .models import Category

# Create your views here.
from rest_framework import viewsets
from .serializers import CategorySerializer
from rest_framework import filters
import django_filters.rest_framework


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('deptcode','mcode','code','description')
    serializer_class = CategorySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['deptcode','mcode','code','description'] 
    search_fields = ['code','description']