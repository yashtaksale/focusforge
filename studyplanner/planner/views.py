from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Subject, StudySession
from .serializers import SubjectSerializer, StudySessionSerializer
from .services import generate_timetable


def get_default_user():
    return User.objects.first()


@api_view(["POST"])
def create_subject(request):
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=get_default_user())
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["POST"])
def generate_plan(request):
    generate_timetable(get_default_user())
    return Response({"message": "Timetable generated successfully"})


@api_view(["GET"])
def get_sessions(request):
    sessions = StudySession.objects.filter(
        subject__user=get_default_user()
    )
    serializer = StudySessionSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def mark_completed(request, session_id):
    session = StudySession.objects.get(id=session_id)
    session.completed = True
    session.save()
    return Response({"message": "Session marked completed"})


@api_view(["GET"])
def progress(request):
    sessions = StudySession.objects.filter(
        subject__user=get_default_user()
    )
    total = sessions.count()
    completed = sessions.filter(completed=True).count()

    percentage = (completed / total * 100) if total > 0 else 0

    return Response({
        "total_sessions": total,
        "completed_sessions": completed,
        "progress_percentage": round(percentage, 2)
    })