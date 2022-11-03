from .models import ItemmasterListedBranch
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterListedBranchSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterListedBranch
 #      depth = 1
        fields = '__all__'