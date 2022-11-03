from .models import Sichild
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class SichildSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Sichild
 #      depth = 1
        fields = '__all__'