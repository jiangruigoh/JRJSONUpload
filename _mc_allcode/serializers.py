from .models import Allcode
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class AllcodeSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Allcode
 #      depth = 1
        fields = '__all__'