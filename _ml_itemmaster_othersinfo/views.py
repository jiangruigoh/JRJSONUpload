from django.shortcuts import render

# Create your views here.
from .models import ItemmasterOthersinfo

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterOthersinfoSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterOthersinfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterOthersinfo.objects.all().order_by('itemcode')
    serializer_class = ItemmasterOthersinfoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode'] 
    search_fields = ['itemcode']	