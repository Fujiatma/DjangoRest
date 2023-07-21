from rest_framework import serializers
from .models import Product, Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['name', 'height', 'stock', 'price', 'weight', 'active_time', 'is_active', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'variants', 'is_active', 'created_at']

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        product = Product.objects.create(**validated_data)
        for variant_data in variants_data:
            Variant.objects.create(product=product, **variant_data)
        return product