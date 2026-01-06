from django.urls import path

from pickbazar.app.views.settings.base import SettingsViewSet

urlpatterns = [
    path('settings/', SettingsViewSet.as_view(), name="settings"),
]
