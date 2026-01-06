from django.urls import path

from pickbazar.app.views.attribute.base import AttributeViewSet

urlpatterns = [
    path(
        "attributes/",
        AttributeViewSet.as_view({"get": "list", "post": "create"}),
        name="attribute",
    ),
    path(
        "attributes/<uuid:pk>/",
        AttributeViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="attribute",
    ),
]
