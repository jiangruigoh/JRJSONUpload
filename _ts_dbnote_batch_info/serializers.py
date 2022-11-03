from .models import DbnoteBatchInfo
from rest_framework import serializers
#from subdept.serializers import subdeptserializer
 
 
class DbnoteBatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbnoteBatchInfo
        fields = '__all__'
