from django.shortcuts import render

# Create your views here.
from .models import ItemmasterReplenishment

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterReplenishmentSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterReplenishmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterReplenishment.objects.all().order_by('itemcode','concept')
    serializer_class = ItemmasterReplenishmentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','concept'] 
    search_fields = ['itemcode','concept']		