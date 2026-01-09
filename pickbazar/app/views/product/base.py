from django.db import IntegrityError
from django.utils.text import slugify
from rest_framework import status
from rest_framework.response import Response

from pickbazar.app.serializers.product import ProductListSerializer, ProductSerializer
from pickbazar.app.views.base import BaseViewSet
from pickbazar.db.models import Product


# Create your views here.
class ProductViewSet(BaseViewSet):
    model = Product
    serializer_class = ProductListSerializer

    search_fields = []
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related('type'))
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            if Product.objects.filter(
                    slug=slugify(request.data.get('name'))
            ).exists():
                return Response(
                    {"name": "The product with the name already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ProductSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(
                [serializer.errors[error][0] for error in serializer.errors],
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"slug": "The product with the slug already exists"},
                    status=status.HTTP_409_CONFLICT,
                )

    def update(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs["slug"])
        if product.name != request.data.get('name'):
            if Product.objects.filter(
                    slug=slugify(request.data.get('name'))
            ).exists():
                return Response(
                    {"name": "The product with the name already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        output = ProductListSerializer(product, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
