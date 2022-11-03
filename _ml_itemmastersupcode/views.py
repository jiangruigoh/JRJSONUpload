from django.shortcuts import render

# Create your views here.
from .models import Itemmastersupcode

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmastersupcodeSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmastersupcodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Itemmastersupcode.objects.all().order_by('itemcode','code')
    serializer_class = ItemmastersupcodeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','code'] 
    search_fields = ['itemcode','code']	