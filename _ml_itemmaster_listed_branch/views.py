from django.shortcuts import render

# Create your views here.
from .models import ItemmasterListedBranch

# Create your views here.
from rest_framework import viewsets
from .serializers import ItemmasterListedBranchSerializer
from rest_framework import filters
import django_filters.rest_framework


class ItemmasterListedBranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemmasterListedBranch.objects.all().order_by('itemcode','branch','itemtype')
    serializer_class = ItemmasterListedBranchSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['itemcode','branch','itemtype'] 
    search_fields = ['itemcode','branch','itemtype']												