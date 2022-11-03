from rest_framework import serializers

class YourSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   comments = serializers.IntegerField()
   likes = serializers.IntegerField()


class PnLSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   date_from = serializers.DateField()
   date_to = serializers.DateField('%Y-%m-%d')