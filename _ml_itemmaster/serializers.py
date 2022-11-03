from .models import Itemmaster
from rest_framework import serializers
from _ml_itembarcode.serializers import ItembarcodeSerializer


class ItemmasterSerializer(serializers.ModelSerializer):
    itembarcode_itemmaster_key = ItembarcodeSerializer(many=True, read_only=True)
    class Meta:
        model = Itemmaster
 #      depth = 1
        fields = '__all__'