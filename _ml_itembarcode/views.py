from django.shortcuts import render

# Create your views here.
from .models import Itembarcode

# Create your views here.
from rest_framework import viewsets
from .serializers import ItembarcodeSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItembarcodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Itembarcode.objects.all().order_by('itemcode','barcode')
    serializer_class = ItembarcodeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','barcode'] 
    search_fields = ['itemcode','barcode']	