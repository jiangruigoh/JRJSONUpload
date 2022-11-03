from .models import Simain
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class SimainSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Simain
 #      depth = 1
        fields = '__all__'