from .models import Locationgroup
from rest_framework import serializers
from _ml_location.serializers import LocationSerializer


class LocationgroupSerializer(serializers.ModelSerializer):
    location_locationgroup_key = LocationSerializer(many=True, read_only=True)
    class Meta:
        model = Locationgroup
 #      depth = 1
        fields = '__all__'