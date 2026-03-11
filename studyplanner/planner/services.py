import logging
import math
from datetime import date, timedelta, datetime, time
from .models import StudySession

logger = logging.getLogger(__name__)

DIFFICULTY_MULTIPLIERS = {1: 1.0, 2: 2.0, 3: 3.5}
CONCENTRATION_FACTORS  = [(3, 1.5), (7, 1.2)]

# Study time slots — morning, afternoon, evening blocks
STUDY_SLOTS = [
    (time(6, 0),  time(8, 0)),   # 6AM–8AM
    (time(9, 0),  time(11, 0)),  # 9AM–11AM
    (time(12, 0), time(14, 0)),  # 12PM–2PM
    (time(15, 0), time(17, 0)),  # 3PM–5PM
    (time(18, 0), time(20, 0)),  # 6PM–8PM
    (time(20, 0), time(22, 0)),  # 8PM–10PM
]


def get_concentration_factor(days_until_exam: int) -> float:
    for threshold, factor in CONCENTRATION_FACTORS:
        if days_until_exam <= threshold:
            return factor
    return 1.0


def calculate_priority(subject) -> float:
    days_left = subject.days_left
    if not days_left or days_left <= 0:
        return 0.0
    return round(
        (10 / days_left)
        + (subject.difficulty * 2)
        + ((100 - subject.syllabus_completion) / 10),
        4
    )


def _compute_subject_weights(subjects) -> dict:
    return {
        s.id: DIFFICULTY_MULTIPLIERS.get(s.difficulty, 1.0)
               * s.daily_hours_available
        for s in subjects
        if s.days_left > 0
    }


def _assign_time_slots(subjects_with_hours: list, day_offset: int) -> list:
    """
    Assign actual start/end times to each subject for a given day.
    Harder/more urgent subjects get prime morning slots.
    Returns list of (subject, start_time, end_time, hours) tuples.
    """
    # Sort by priority — most urgent gets first slot
    sorted_subjects = sorted(
        subjects_with_hours,
        key=lambda x: calculate_priority(x[0]),
        reverse=True
    )

    assignments = []
    slot_index  = 0

    for subject, hours in sorted_subjects:
        if slot_index >= len(STUDY_SLOTS):
            slot_index = 0  # wrap around if many subjects

        start = STUDY_SLOTS[slot_index][0]
        # Calculate end time based on allocated hours
        start_dt = datetime.combine(date.today(), start)
        end_dt   = start_dt + timedelta(hours=hours)
        end      = end_dt.time()

        # Make sure we don't go past midnight
        if end_dt.date() > date.today():
            end = time(23, 59)

        assignments.append((subject, start, end, hours))
        slot_index += 1

    return assignments


def get_study_approach(subject_name: str, difficulty: int) -> dict:
    """
    Returns a structured study approach for a subject
    based on its name and difficulty level.
    """
    difficulty_tips = {
        1: {
            "approach": "Light Review",
            "sessions":  "1–2 focused sessions per day",
            "technique": "Spaced repetition + quick quizzes",
        },
        2: {
            "approach": "Active Learning",
            "sessions":  "2–3 sessions with breaks",
            "technique": "Pomodoro (25min study / 5min break)",
        },
        3: {
            "approach": "Deep Work",
            "sessions":  "3–4 intensive sessions",
            "technique": "Feynman technique + practice problems",
        },
    }

    name_lower = subject_name.lower()

    # Subject-specific steps
    if any(k in name_lower for k in ["math", "calculus", "algebra", "statistics"]):
        steps = [
            "Review theory and formulas first",
            "Solve 5 easy problems to warm up",
            "Attempt past exam questions",
            "Identify weak areas and re-study",
            "Timed mock test before exam",
        ]
    elif any(k in name_lower for k in ["code", "program", "python", "java", "algorithm", "data structure"]):
        steps = [
            "Read concept documentation",
            "Type out examples by hand (no copy-paste)",
            "Solve 3 LeetCode/practice problems",
            "Build a small working demo",
            "Review time/space complexity",
        ]
    elif any(k in name_lower for k in ["history", "social", "geography", "civics"]):
        steps = [
            "Create a timeline of key events",
            "Make mind maps for each chapter",
            "Write short summaries in own words",
            "Practice with flashcards",
            "Answer previous year questions",
        ]
    elif any(k in name_lower for k in ["physics", "chemistry", "biology", "science"]):
        steps = [
            "Understand diagrams and processes",
            "Memorize key formulas/reactions",
            "Solve numerical problems",
            "Draw and label diagrams from memory",
            "Revise with chapter summary notes",
        ]
    elif any(k in name_lower for k in ["english", "language", "writing", "literature"]):
        steps = [
            "Read chapter/poem carefully once",
            "Note down key themes and characters",
            "Practice grammar exercises",
            "Write one essay/paragraph for practice",
            "Review model answers",
        ]
    else:
        steps = [
            "Read through all notes/textbook once",
            "Highlight and summarize key points",
            "Create flashcards for important terms",
            "Test yourself with past questions",
            "Final quick revision 1 day before",
        ]

    tips = difficulty_tips.get(difficulty, difficulty_tips[2])
    return {
        "approach":  tips["approach"],
        "sessions":  tips["sessions"],
        "technique": tips["technique"],
        "steps":     steps,
    }


def generate_timetable(user) -> dict:
    subjects = list(user.subjects.select_related().all())
    StudySession.objects.filter(subject__user=user).delete()

    if not subjects:
        logger.warning("generate_timetable: no subjects for user %s", user.id)
        return {"sessions_created": 0, "skipped_subjects": [], "timetable": []}

    skipped        = [s.name for s in subjects if s.is_exam_passed]
    valid_subjects = [s for s in subjects if not s.is_exam_passed]

    if not valid_subjects:
        return {"sessions_created": 0, "skipped_subjects": skipped, "timetable": []}

    max_days = max(s.days_left for s in valid_subjects)
    if max_days <= 0:
        return {"sessions_created": 0, "skipped_subjects": skipped, "timetable": []}

    sessions_to_create = []
    timetable_preview  = []  # rich data for frontend
    today = date.today()

    for day_offset in range(max_days):
        current_date    = today + timedelta(days=day_offset)
        active_subjects = [s for s in valid_subjects if s.days_left > day_offset]
        if not active_subjects:
            continue

        daily_weights = _compute_subject_weights(active_subjects)
        total_weight  = sum(daily_weights.values())

        # Build (subject, hours) pairs for this day
        day_subjects = []
        for subject in active_subjects:
            weight          = daily_weights.get(subject.id, 0)
            base_hours      = (weight / total_weight * subject.daily_hours_available
                               if total_weight else
                               subject.daily_hours_available / len(active_subjects))
            days_until_exam = subject.days_left - day_offset
            final_hours     = round(base_hours * get_concentration_factor(days_until_exam), 2)
            day_subjects.append((subject, final_hours))

        # Assign real time slots
        assignments = _assign_time_slots(day_subjects, day_offset)

        for subject, start_time, end_time, hours in assignments:
            sessions_to_create.append(
                StudySession(
                    subject=subject,
                    date=current_date,
                    hours_allocated=hours,
                    notes=f"{start_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}",
                )
            )

            # Only send first 14 days to frontend preview
            if day_offset < 14:
                approach = get_study_approach(subject.name, subject.difficulty)
                timetable_preview.append({
                    "date":         current_date.strftime("%d %b %Y"),
                    "day":          current_date.strftime("%A"),
                    "subject":      subject.name,
                    "priority":     subject.priority_label,
                    "days_left":    subject.days_left - day_offset,
                    "start_time":   start_time.strftime("%I:%M %p"),
                    "end_time":     end_time.strftime("%I:%M %p"),
                    "hours":        hours,
                    "approach":     approach["approach"],
                    "technique":    approach["technique"],
                    "steps":        approach["steps"],
                    "difficulty":   subject.difficulty,
                })

    StudySession.objects.bulk_create(sessions_to_create)
    logger.info("generate_timetable: created %d sessions for user %s",
                len(sessions_to_create), user.id)

    return {
        "sessions_created": len(sessions_to_create),
        "skipped_subjects": skipped,
        "timetable":        timetable_preview,
    }