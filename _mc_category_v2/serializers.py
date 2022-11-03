from .models import Category
from rest_framework import serializers
#from subdept.serializers import subdeptserializer


class CategorySerializer(serializers.ModelSerializer):
 #       subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Category
 #      depth = 1
        fields = '__all__'