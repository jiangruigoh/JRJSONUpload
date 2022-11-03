from .models import ItemmasterItemtype
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterItemtypeSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterItemtype
 #      depth = 1
        fields = '__all__'