from rest_framework import serializers

from pickbazar.db.models import Attribute, AttributeValue


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class AttributeValueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'
