from rest_framework import serializers

from pickbazar.db.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
