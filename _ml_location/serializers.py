from .models import Location
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class LocationSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Location
 #      depth = 1
        fields = '__all__'