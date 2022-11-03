from django.shortcuts import render

# Create your views here.
from .models import ItemmasterBlockByBranch

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterBlockByBranchSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterBlockByBranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterBlockByBranch.objects.all().order_by('itemcode','branch')
    serializer_class = ItemmasterBlockByBranchSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','branch'] 
    search_fields = ['itemcode','branch']	