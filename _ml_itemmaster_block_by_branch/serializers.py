from .models import ItemmasterBlockByBranch
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterBlockByBranchSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterBlockByBranch
 #      depth = 1
        fields = '__all__'