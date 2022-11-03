from django.shortcuts import render

# Create your views here.
from .models import ItemmasterMiscellaneous

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterMiscellaneousSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterMiscellaneousViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterMiscellaneous.objects.all().order_by('itemcode','mis_guid')
    serializer_class = ItemmasterMiscellaneousSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','mis_guid'] 
    search_fields = ['itemcode','mis_guid']	