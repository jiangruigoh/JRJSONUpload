from django.shortcuts import render

# Create your views here.
from .models import ItemmasterBranchStock

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterBranchStockSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterBranchStockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterBranchStock.objects.all().order_by('itemcode','branch',)
    serializer_class = ItemmasterBranchStockSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','branch'] 
    search_fields = ['itemcode','branch']	