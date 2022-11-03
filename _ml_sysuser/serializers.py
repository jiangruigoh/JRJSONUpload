from .models import Sysuser
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class SysuserSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Sysuser
 #      depth = 1
        fields = '__all__'