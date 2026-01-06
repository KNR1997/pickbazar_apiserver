from django.urls import path

from pickbazar.app.views.product.base import ProductViewSet

urlpatterns = [
    path(
        "products/",
        ProductViewSet.as_view({"get": "list", "post": "create"}),
        name="product",
    ),
    path(
        "products/<str:slug>/",
        ProductViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="product",
    ),
]
