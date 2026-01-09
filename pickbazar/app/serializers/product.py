from django.utils.text import slugify
from rest_framework import serializers

from pickbazar.app.serializers.author import AuthorListSerializer
from pickbazar.app.serializers.base import BaseSerializer
from pickbazar.app.serializers.category import CategoryListSerializer
from pickbazar.app.serializers.manufacturer import ManufacturerListSerializer
from pickbazar.app.serializers.tag import TagListSerializer
from pickbazar.app.serializers.type import TypeListSerializer
from pickbazar.db.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ["slug"]

    def create(self, validated_data):
        # slugify name to be used on Product create
        slug = slugify(validated_data.get("name"))

        # create Product
        validated_data['slug'] = slug
        return super().create(validated_data)

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
