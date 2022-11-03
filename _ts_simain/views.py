from logging import raiseExceptions
from multiprocessing.sharedctypes import Value
from django.shortcuts import render

# Create your views here.
from .models import Simain

# Create your views here.
from rest_framework import viewsets
from .serializers import SimainSerializer
from rest_framework import filters
import django_filters.rest_framework
from _lib.panda import refno_seq_gen 
from django.db.models import Max
from rest_framework.response import Response


class SimainViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Simain.objects.all().order_by('refno','invoicedate')
    serializer_class = SimainSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_fields = ['refno','docno','invoicedate','code','billstatus','deflocation'] 
    search_fields = ['refno','docno','invoicedate','code','name','billstatus','deflocation']
    region_separator = ","


    def get_queryset(self):
        refno_i = self.request.query_params.get("refno_i", None)
        if refno_i:
            qs = Simain.objects.filter()
            for region in refno_i.split(self.region_separator):
                qs = qs.filter(refno__contains=region)
            last_index = len(qs)
            start_index = len(qs)-1
            return qs.values()[start_index:last_index]
        return super().get_queryset()


    def create(self, request, *args, **kwargs):
        lastest_refno = Simain.objects.all().aggregate(Max('refno'))
        
        #Simain.objects.create()
        #print(request.data)
        new_json = request.data
        # print(lastest_refno)

        new_refno = refno_seq_gen(lastest_refno["refno__max"])
        #print(new_refno)
        new_json.update({"refno": new_refno})
        

        serializer = self.get_serializer(data=new_json)
        serializer.is_valid(raise_exception=True)
        #print(new_json)
        self.perform_create(serializer)

        return Response({"status": "success", "pk": serializer.instance.pk})

