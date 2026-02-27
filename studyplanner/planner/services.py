from datetime import date, timedelta
from .models import StudySession


def calculate_priority(subject):
    days_left = subject.days_left()
    if days_left <= 0:
        return 0

    urgency = 10 / days_left
    difficulty_weight = subject.difficulty * 2
    syllabus_weight = (100 - subject.syllabus_completion) / 10

    return urgency + difficulty_weight + syllabus_weight


def generate_timetable(user):
    subjects = user.subject_set.all()

    # Clear previous sessions
    StudySession.objects.filter(subject__user=user).delete()

    today = date.today()

    max_days = max(
        [s.days_left() for s in subjects if s.days_left() > 0],
        default=0
    )

    for day in range(max_days):
        current_date = today + timedelta(days=day)

        active_subjects = [
            s for s in subjects if s.days_left() > day
        ]

        if not active_subjects:
            continue

        priorities = {s: calculate_priority(s) for s in active_subjects}
        total_priority = sum(priorities.values())

        for subject in active_subjects:
            hours = (
                priorities[subject] / total_priority
            ) * subject.daily_hours_available

            StudySession.objects.create(
                subject=subject,
                date=current_date,
                hours_allocated=round(hours, 2)
            )