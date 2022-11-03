from .models import ItemmasterPricetype
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterPricetypeSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterPricetype
 #      depth = 1
        fields = '__all__'