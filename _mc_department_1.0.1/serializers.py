from .models import Department
from rest_framework import serializers
from _mc_subdept.serializers import SubdeptSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    subdept_key = SubdeptSerializer(many=True, read_only=True)
    class Meta:
        model = Department
 #      depth = 1
        fields = '__all__'