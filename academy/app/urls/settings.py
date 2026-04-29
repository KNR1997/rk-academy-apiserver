from django.urls import path

from academy.app.views.settings.base import SettingsViewSet

urlpatterns = [
    path('settings/', SettingsViewSet.as_view(), name="settings"),
]
