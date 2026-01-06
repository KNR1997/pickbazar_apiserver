from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from pickbazar.app.serializers.category import CategoryListSerializer, CategoryCreateSerializer, \
    CategoryUpdateSerializer
from pickbazar.app.views.base import BaseViewSet
from pickbazar.db.models import Category


# Create your views here.
class CategoryViewSet(BaseViewSet):
    model = Category
    serializer_class = CategoryListSerializer

    search_fields = []
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset().select_related("type"))
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        category = self.get_queryset().filter(slug=slug).first()

        if not category:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryListSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            serializer = CategoryCreateSerializer(data=request.data)

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
                    {"slug": "The category with the slug already exists"},
                    status=status.HTTP_409_CONFLICT,
                )

    def update(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs["slug"])

        serializer = CategoryUpdateSerializer(
            category,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()

        output = CategoryListSerializer(category, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
