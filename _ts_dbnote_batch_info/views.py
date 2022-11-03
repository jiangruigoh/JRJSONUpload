from django.shortcuts import render

# Create your views here.
from .models import DbnoteBatchInfo
 
# Create your views here.
from rest_framework import viewsets
from .serializers import DbnoteBatchInfoSerializer
from rest_framework import filters
import django_filters.rest_framework
 
 
class DbnoteBatchInfoViewSet(viewsets.ModelViewSet):
     """
     API endpoint that allows users to be viewed or edited.
     """
     queryset = DbnoteBatchInfo.objects.all().order_by('batch_no')
     serializer_class = DbnoteBatchInfoSerializer
     filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
#     filterset_fields = ['subdept_guid','dept_guid','code','description'] 
     filterset_fields = {
         'dbnote_guid':["in","exact"],
         'customer_guid' : ["in","exact"],
         'batch_no': ["in","exact"],
         'sup_code':["in","exact"],
         'sup_name':["in","exact"],
         'b2b_dn_refno':["in","exact"],
         'location':["in","exact"],
         'sub_location':["in","exact"],
         'sup_code':["in","exact"],
         'loc_group':["in","exact"]
         }
     search_fields = ['dbnote_guid','customer_guid','batch_no','sup_code','sup_name','b2b_no_refno',
     'location','sub_location','sup_code','loc_group']