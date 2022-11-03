from django.shortcuts import render

# Create your views here.
from .models import SetGroup

# Create your views here.
from rest_framework import viewsets
from .serializers import SetGroupSerializer
from rest_framework import filters
import django_filters.rest_framework


class SetGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SetGroup.objects.all().order_by('group_code','group_desc','created_at','created_by','updated_at','updated_by')
    serializer_class = SetGroupSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['group_code','group_desc','created_at','created_by','updated_at','updated_by'] 
    search_fields = ['group_code','group_desc','created_at','created_by','updated_at','updated_by']