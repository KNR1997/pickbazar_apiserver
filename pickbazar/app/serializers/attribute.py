from django.utils.text import slugify
from rest_framework import serializers

from pickbazar.app.serializers.base import BaseSerializer
from pickbazar.db.models import Attribute, AttributeValue


class AttributeCreateSerializer(BaseSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
        read_only_fields = ['slug']

    def create(self, validated_data):
        return super().create(validated_data)


class AttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = AttributeValue
        fields = '__all__'
        read_only_fields = ["attribute"]


class AttributeValueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
        read_only_fields = ["slug"]

    # Nested serializer
    values = AttributeValueSerializer(many=True)

    # Custom create()
    def create(self, validated_data):
        # First we create the Attribute
        values = validated_data.pop("values")
        slug = slugify(validated_data.get("name"))

        attribute = Attribute.objects.create(slug=slug, **validated_data)
        AttributeValue.objects.bulk_create(
            [
                AttributeValue(
                    attribute=attribute,
                    value=attribute_value.get('value'),
                    meta=attribute_value.get('value'),
                )
                for attribute_value in values
            ]
        )
        return attribute

    def update(self, instance, validated_data):
        values = validated_data.pop("values", [])
        slug = slugify(validated_data.get("name"))

        attribute = Attribute.objects.filter(
            id=instance.id
        ).update(
            slug=slug,
            **validated_data
        )

        for value in values:
            AttributeValue.objects.filter(
                id=value['id'],
                attribute=attribute,
            ).update(
                value=value.get("value"),
                meta=value.get("meta"),
            )
        return attribute


class AttributeListSerializer(serializers.ModelSerializer):
    values = AttributeValueListSerializer(many=True)

    class Meta:
        model = Attribute
        fields = '__all__'
