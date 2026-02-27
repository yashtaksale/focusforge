from django.urls import path
from . import views

urlpatterns = [
    path("subject/create/", views.create_subject),
    path("generate/", views.generate_plan),
    path("sessions/", views.get_sessions),
    path("complete/<int:session_id>/", views.mark_completed),
    path("progress/", views.progress),
]