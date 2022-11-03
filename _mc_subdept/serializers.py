from .models import Subdept
from rest_framework import serializers
from _mc_category.serializers import CategorySerializer


class SubdeptSerializer(serializers.ModelSerializer):
    category_key = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Subdept
 #      depth = 1
        fields = '__all__'