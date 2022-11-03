from .models import SetGroupDept
from rest_framework import serializers
#from _mc_department.serializers import DepartmentSerializer


class SetGroupDeptSerializer(serializers.ModelSerializer):
#    department_key = DepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = SetGroupDept
 #      depth = 1
        fields = '__all__'