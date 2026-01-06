from rest_framework import serializers

from pickbazar.app.serializers.base import BaseSerializer
from pickbazar.app.serializers.type import TypeListSerializer
from pickbazar.db.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ManufacturerListSerializer(serializers.ModelSerializer):
    type = TypeListSerializer()

    class Meta:
        model = Manufacturer
        fields = '__all__'


class ManufacturerCreateSerializer(BaseSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class ManufacturerUpdateSerializer(BaseSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
