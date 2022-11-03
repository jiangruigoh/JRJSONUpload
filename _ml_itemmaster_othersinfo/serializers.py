from .models import ItemmasterOthersinfo
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class ItemmasterOthersinfoSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = ItemmasterOthersinfo
 #      depth = 1
        fields = '__all__'