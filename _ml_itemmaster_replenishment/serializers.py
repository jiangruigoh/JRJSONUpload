from .models import ItemmasterReplenishment
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterReplenishmentSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterReplenishment
 #      depth = 1
        fields = '__all__'