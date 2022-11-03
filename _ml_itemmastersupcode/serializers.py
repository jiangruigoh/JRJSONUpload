from .models import Itemmastersupcode
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmastersupcodeSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Itemmastersupcode
 #      depth = 1
        fields = '__all__'