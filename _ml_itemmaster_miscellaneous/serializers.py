from .models import ItemmasterMiscellaneous
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterMiscellaneousSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterMiscellaneous
 #      depth = 1
        fields = '__all__'