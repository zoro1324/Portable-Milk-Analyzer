from rest_framework import serializers

class MilkSubmissionRequestSerializer(serializers.Serializer):
    rf_no = serializers.CharField(max_length=50)
    image = serializers.ImageField()
