from rest_framework import serializers

from pickbazar.db.models import Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class TypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
