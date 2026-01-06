from rest_framework import serializers

from pickbazar.app.serializers.base import BaseSerializer
from pickbazar.app.serializers.type import TypeListSerializer
from pickbazar.db.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    type = TypeListSerializer()

    class Meta:
        model = Tag
        fields = '__all__'


class TagCreateSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class TagUpdateSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
