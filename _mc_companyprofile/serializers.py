from .models import Companyprofile
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class CompanyprofileSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Companyprofile
 #      depth = 1
        fields = '__all__'