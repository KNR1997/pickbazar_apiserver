from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from pickbazar.app.serializers.author import AuthorListSerializer
from pickbazar.app.serializers.category import CategoryListSerializer
from pickbazar.app.serializers.manufacturer import ManufacturerListSerializer
from pickbazar.app.serializers.tag import TagListSerializer
from pickbazar.app.serializers.type import TypeListSerializer
from pickbazar.db.models import Product, Attribute, AttributeValue
from pickbazar.db.models.product import ProductVariation


class OptionSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class UpsertSerializer(serializers.Serializer):
    title = serializers.CharField()
    sku = serializers.CharField()
    options = OptionSerializer(many=True)


class VariationOptionsSerializer(serializers.Serializer):
    upsert = UpsertSerializer(many=True)


class ProductSerializer(serializers.ModelSerializer):
    # non-related Attribute field (pop before create or update)
    variation_options = VariationOptionsSerializer(required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ["slug"]

    def create(self, validated_data):
        with transaction.atomic():
            # pop all the non-related Attribute fields from the validated_data
            variation_options = validated_data.pop("variation_options")

            # slugify name to be used on Product create
            slug = slugify(validated_data.get("name"))

            # create Product
            validated_data['slug'] = slug
            product = super().create(validated_data)

            for upsert in variation_options.get('upsert', []):
                options = upsert.get('options', [])

                attribute_list = []
                attribute_value_list = []

                for option in options:
                    attribute = Attribute.objects.filter(name=option.get('name')).first()
                    attribute_list.append(attribute)
                    attribute_value = AttributeValue.objects.filter(value=option.get('value')).first()
                    attribute_value_list.append(attribute_value)

                product_variation = ProductVariation.objects.create(
                    title=upsert.get('title'),
                    product=product,
                )

                product_variation.attribute.set(attribute_list)
                product_variation.value.set(attribute_value_list)

            return product

    def update(self, instance, validated_data):
        slug = slugify(validated_data.get('name'))
        validated_data['slug'] = slug
        return super().update(instance, validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    author = AuthorListSerializer()
    manufacturer = ManufacturerListSerializer()
    type = TypeListSerializer()
    categories = CategoryListSerializer(many=True)
    tags = TagListSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
