from django.shortcuts import render

# Create your views here.
from .models import SetGroupDept

# Create your views here.
from rest_framework import viewsets
from .serializers import SetGroupDeptSerializer
from rest_framework import filters
import django_filters.rest_framework


class SetGroupDeptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SetGroupDept.objects.all().order_by('group_code','dept_code','dept_desc')
    serializer_class = SetGroupDeptSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['group_code','dept_code','dept_desc'] 
    search_fields = ['group_code','dept_code','dept_desc']	