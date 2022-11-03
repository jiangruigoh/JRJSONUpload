from .models import Subdept
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class SubdeptSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Subdept
 #      depth = 1
        fields = '__all__'