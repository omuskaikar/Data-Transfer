from rest_framework import serializers

class DbConnectionSerializer(serializers.Serializer):
    host = serializers.CharField(max_length=255)  # Changed from 'ip' to 'host'
    user = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

