from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.planner.views import home_page, focus_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home_page, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("apps.planner.urls")),
    path("focus/", focus_page, name="focus"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/login/"),
        name="logout",
    ),
]
