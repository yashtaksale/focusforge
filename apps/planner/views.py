# planner/views.py
import logging
from datetime import date
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from .models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer
from .services import generate_timetable
from django.utils import timezone


logger = logging.getLogger(__name__)


def home_page(request):
    return render(request, "index.html")


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def subjects(request):
    if request.method == "GET":
        qs = Subject.objects.filter(user=request.user)
        return Response(SubjectSerializer(qs, many=True).data)

    name = request.data.get("name", "").strip()
    existing = Subject.objects.filter(user=request.user, name__iexact=name).first()
    if existing:
        serializer = SubjectSerializer(existing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Timetable Generation ──────────────────────────────────────
@api_view(["POST"])
@permission_classes([AllowAny])
def generate_plan(request):
    result = generate_timetable(request.user)

    response_data = {
        "message":          "Timetable generated successfully",
        "sessions_created": result["sessions_created"],
        "timetable":        result["timetable"],
    }
    if result["skipped_subjects"]:
        response_data["warning"] = (
            f"Skipped subjects with past exam date: "
            f"{', '.join(result['skipped_subjects'])}"
        )

    return Response(response_data, status=status.HTTP_201_CREATED)


# ─── Sessions ─────────────────────────────────────────────────
@api_view(["GET"])
@permission_classes([AllowAny])
def get_sessions(request):
    qs = StudySession.objects.filter(
        subject__user=request.user
    ).select_related("subject").order_by("date", "id")

    date_str = request.GET.get("date")
    if date_str:
        qs = qs.filter(date=date_str)

    return Response(StudySessionSerializer(qs, many=True).data)


@api_view(["PATCH"])
@permission_classes([AllowAny])
def mark_completed(request, session_id):
    session = get_object_or_404(
        StudySession,
        id=session_id,
        subject__user=request.user
    )

    # Allow toggling completion
    session.completed = not session.completed
    session.completed_at = timezone.now() if session.completed else None
    session.save(update_fields=["completed", "completed_at"])

    return Response({
        "message": f"Session marked as {'completed' if session.completed else 'pending'}",
        "completed": session.completed,
    })


# ─── Progress ─────────────────────────────────────────────────
@api_view(["GET"])
@permission_classes([AllowAny])
def progress(request):
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
@permission_classes([AllowAny])
def daily_progress(request):
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


# ─── PDF Export ───────────────────────────────────────────────
def export_pdf(request):
    sessions = (
        StudySession.objects
        .filter(subject__user=request.user)
        .select_related("subject")
        .order_by("date")
    )

    buffer = BytesIO()
    doc    = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm, leftMargin=15*mm,
        topMargin=15*mm,   bottomMargin=15*mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontSize=24,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#ff6b6b"),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    sub_style = ParagraphStyle(
        "Sub",
        parent=styles["Normal"],
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#7a6652"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#2d2013"),
        spaceBefore=12,
        spaceAfter=6,
    )
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontSize=8,
        fontName="Helvetica",
        alignment=TA_CENTER,
    )
    cell_bold = ParagraphStyle(
        "CellBold",
        parent=styles["Normal"],
        fontSize=8,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )

    story = []
    username = request.user.username if getattr(request, "user", None) and request.user.is_authenticated else "Student"

    # Header
    story.append(Paragraph("FocusForge Study Plan", title_style))
    story.append(Paragraph(f"Study Plan for {username}", sub_style))
    story.append(Paragraph(f"Generated on {date.today().strftime('%B %d, %Y')}", sub_style))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#ff6b6b")))
    story.append(Spacer(1, 4*mm))

    # Group sessions by date
    by_date = {}
    for s in sessions:
        key = str(s.date)
        if key not in by_date:
            by_date[key] = []
        by_date[key].append(s)

    if not by_date:
        story.append(Paragraph("No sessions found. Add subjects and generate a plan first!", styles["Normal"]))
    else:
        for date_str, day_sessions in by_date.items():
            try:
                from datetime import datetime
                d = datetime.strptime(date_str, "%Y-%m-%d")
                day_label = d.strftime("%A, %B %d %Y")
            except Exception:
                day_label = date_str

            story.append(Paragraph(f"Schedule: {day_label}", section_style))

            table_data = [["Time Slot", "Subject", "Hours", "Difficulty", "Urgency", "Status"]]
            diff_map   = {1: "Easy", 2: "Medium", 3: "Hard"}
            status_map = {True: "Completed", False: "Pending"}

            for s in day_sessions:
                table_data.append([
                    Paragraph(s.notes or "—", cell_style),
                    Paragraph(s.subject.name, cell_bold),
                    Paragraph(f"{s.hours_allocated}h", cell_style),
                    Paragraph(diff_map.get(s.subject.difficulty, "Medium"), cell_style),
                    Paragraph(s.subject.priority_label, cell_style),
                    Paragraph(status_map[s.completed], cell_style),
                ])

            col_widths = [45*mm, 45*mm, 18*mm, 24*mm, 24*mm, 24*mm]
            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#ff6b6b")),
                ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
                ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
                ("FONTSIZE",     (0,0), (-1,0), 9),
                ("ALIGN",        (0,0), (-1,-1), "CENTER"),
                ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
                ("BOTTOMPADDING",(0,0), (-1,0), 6),
                ("TOPPADDING",   (0,0), (-1,0), 6),
                ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#fff9f4"), colors.white]),
                ("TOPPADDING",   (0,1), (-1,-1), 5),
                ("BOTTOMPADDING",(0,1), (-1,-1), 5),
                ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#f0e6d8")),
            ]))

            story.append(table)
            story.append(Spacer(1, 4*mm))

    total     = sessions.count()
    completed = sessions.filter(completed=True).count()
    percent   = round(completed / total * 100) if total else 0

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#f0e6d8")))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f"Summary: {completed}/{total} sessions completed ({percent}%)",
        ParagraphStyle("footer", parent=styles["Normal"], fontSize=10,
                       fontName="Helvetica-Bold", textColor=colors.HexColor("#7a6652"),
                       alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="study_plan_{username}.pdf"'
    return response


# ─── Subject Detail (Edit / Delete) ───────────────────────────
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)

    if request.method == "GET":
        return Response(SubjectSerializer(subject).data)

    if request.method == "PUT":
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        subject.delete()
        return Response({"message": "Subject deleted"}, status=status.HTTP_204_NO_CONTENT)


def focus_page(request):
    subject = request.GET.get("subject", "Study Session")
    return render(request, "focus.html", {"subject": subject})
