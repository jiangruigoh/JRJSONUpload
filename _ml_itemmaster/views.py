from django.shortcuts import render

# Create your views here.
from .models import Itemmaster

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Itemmaster.objects.all().order_by('dept','subdept','category','itemlink','itemcode','description')
    serializer_class = ItemmasterSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['dept','subdept','category','itemlink','itemcode','description'] 
    search_fields = ['dept','subdept','category','itemlink','itemcode','description']	