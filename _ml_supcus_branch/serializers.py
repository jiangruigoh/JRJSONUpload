from .models import SupcusBranch
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class SupcusBranchSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = SupcusBranch
 #      depth = 1
        fields = '__all__'