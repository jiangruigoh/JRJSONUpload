from .models import Supcus
from rest_framework import serializers
#from _ml_supcus_branch.serializers import SupcusBranchSerializer


class SupcusSerializer(serializers.ModelSerializer):
    #supcus_branch_key = SupcusBranchSerializer(many=True, read_only=True)
    class Meta:
        model = Supcus
 #      depth = 1
        fields = '__all__'