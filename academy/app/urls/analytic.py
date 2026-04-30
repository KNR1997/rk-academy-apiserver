from django.urls import path

from academy.app.views.analytic.base import InstituteAnalyticsDataEndpoint

urlpatterns = [
    path(
        "analytics/",
        InstituteAnalyticsDataEndpoint.as_view(),
        name="institute-analytics-data",
    ),
]