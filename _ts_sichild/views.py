from django.shortcuts import render

# Create your views here.
from .models import Sichild

# Create your views here.
from rest_framework import viewsets
from .serializers import SichildSerializer
from rest_framework import filters
import django_filters.rest_framework


class SichildViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Sichild.objects.all().order_by('refno','line')
    serializer_class = SichildSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['refno','line','barcode','itemcode','colour','size','brand','articleno','itemlink','dept','subdept','category','location','hq_update','consign','itemtype'] 
    search_fields = ['refno','line','barcode','itemcode','colour','size','brand','articleno','itemlink','dept','subdept','category','location','hq_update','consign','itemtype']	