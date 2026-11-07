from django.contrib import admin
from django.urls import path, include
from apps.planner.views import home_page, focus_page

urlpatterns = [
    path("", home_page, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("apps.planner.urls")),
    path("focus/", focus_page, name="focus"),
]
