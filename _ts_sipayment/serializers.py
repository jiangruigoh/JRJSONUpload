from .models import SiPayment
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class SiPaymentSerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = SiPayment
 #      depth = 1
        fields = '__all__'