from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","is_superuser","is_staff","is_active", "last_login","date_joined"]