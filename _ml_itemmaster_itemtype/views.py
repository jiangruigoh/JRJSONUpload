from django.shortcuts import render

# Create your views here.
from .models import ItemmasterItemtype

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterItemtypeSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterItemtypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterItemtype.objects.all().order_by('itemcode','itemtype')
    serializer_class = ItemmasterItemtypeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','itemtype'] 
    search_fields = ['itemcode','itemtype']	