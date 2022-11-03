from .models import ItemmasterBranchStock
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterBranchStockSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterBranchStock
 #      depth = 1
        fields = '__all__'