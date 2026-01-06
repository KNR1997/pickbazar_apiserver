from rest_framework import serializers

from pickbazar.app.serializers.base import BaseSerializer
from pickbazar.app.serializers.type import TypeListSerializer
from pickbazar.db.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    type = TypeListSerializer()

    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class CategoryUpdateSerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
