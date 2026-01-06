from rest_framework import serializers

from pickbazar.app.serializers.base import BaseSerializer
from pickbazar.db.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'mobile_number', 'email', 'first_name', 'last_name']
