from .models import SetGroup
from rest_framework import serializers
from _mc_set_group_dept.serializers import SetGroupDeptSerializer


class SetGroupSerializer(serializers.ModelSerializer):
    set_group_code_key = SetGroupDeptSerializer(many=True, read_only=True)
    class Meta:
        model = SetGroup
 #      depth = 1
        fields = '__all__'