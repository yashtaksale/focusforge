# planner/views.py
import logging
from datetime import date

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer
from .services import generate_timetable

logger = logging.getLogger(__name__)


# ─── HTML View ────────────────────────────────────────────────
@login_required
def home_page(request):
    return render(request, "index.html")


# ─── Subjects ─────────────────────────────────────────────────
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def subjects(request):
    """
    GET  → list all subjects for current user
    POST → create a new subject
    """
    if request.method == "GET":
        qs = Subject.objects.filter(user=request.user)
        return Response(SubjectSerializer(qs, many=True).data)

    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Timetable Generation ──────────────────────────────────────
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_plan(request):
    result = generate_timetable(request.user)

    response_data = {
        "message":          "Timetable generated successfully",
        "sessions_created": result["sessions_created"],
        "timetable":        result["timetable"],        # ← new
    }
    if result["skipped_subjects"]:
        response_data["warning"] = (
            f"Skipped subjects with no exam date: "
            f"{', '.join(result['skipped_subjects'])}"
        )

    return Response(response_data, status=status.HTTP_201_CREATED)


# ─── Sessions ─────────────────────────────────────────────────
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_sessions(request):
    """
    Returns sessions for current user.
    Optional filter: ?date=YYYY-MM-DD
    """
    qs = StudySession.objects.filter(
        subject__user=request.user
    ).select_related("subject").order_by("date")

    date_str = request.GET.get("date")
    if date_str:
        qs = qs.filter(date=date_str)

    return Response(StudySessionSerializer(qs, many=True).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_completed(request, session_id):
    """Mark a session as completed. PATCH is correct — partial update."""
    session = get_object_or_404(
        StudySession,
        id=session_id,
        subject__user=request.user
    )
    session.completed = True
    session.save(update_fields=["completed"])
    return Response({"message": "Session marked as completed"})


# ─── Progress ─────────────────────────────────────────────────
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def progress(request):
    """
    Overall or single-day progress.
    Optional: ?date=YYYY-MM-DD
    """
    qs = StudySession.objects.filter(subject__user=request.user)

    date_str = request.GET.get("date")
    if date_str:
        qs = qs.filter(date=date_str)

    total     = qs.count()
    completed = qs.filter(completed=True).count()
    percent   = round(completed / total * 100, 2) if total else 0

    return Response({
        "date":                date_str or None,
        "total_sessions":      total,
        "completed_sessions":  completed,
        "progress_percentage": percent,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def daily_progress(request):
    """
    Progress grouped by date — single aggregated DB query.
    """
    stats = (
        StudySession.objects
        .filter(subject__user=request.user)
        .values("date")
        .annotate(
            total=Count("id"),
            completed=Count("id", filter=Q(completed=True)),
        )
        .order_by("date")
    )

    result = {
        str(row["date"]): {
            "total":      row["total"],
            "completed":  row["completed"],
            "percentage": round(row["completed"] / row["total"] * 100, 2)
                          if row["total"] else 0,
        }
        for row in stats
    }

    return Response(result)