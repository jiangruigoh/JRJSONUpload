from django.shortcuts import render

# Create your views here.
from .models import SiPayment

# Create your views here.
from rest_framework import viewsets
from .serializers import SiPaymentSerializer
from rest_framework import filters
import django_filters.rest_framework


class SiPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SiPayment.objects.all().order_by('refno','line')
    serializer_class = SiPaymentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['refno','line','location','bizdate','cardtype','paytype','loc_group'] 
    search_fields = ['refno','line','location','bizdate','cardtype','paytype','loc_group']	