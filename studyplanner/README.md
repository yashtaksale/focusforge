# 📚 Smart Study Planner

A production-grade AI-powered study timetable generator built with Django REST Framework.
Automatically creates personalized, priority-weighted study schedules based on exam dates and subject difficulty.

---

## 🚀 Features

- **Priority-Weighted Algorithm** — harder subjects + closer exams get more study time
- **Smart Time Slots** — assigns real time blocks (e.g. 9AM–11AM) per subject per day
- **Study Strategy Engine** — detects subject type (Math, Physics, Coding etc.) and suggests tailored study steps
- **Progress Tracker** — live progress bar showing overall completion percentage
- **Daily Checklist** — mark sessions complete, grouped by date
- **REST API** — fully decoupled Django REST Framework backend
- **Authentication** — session-based login/logout

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 + Django REST Framework |
| Database | SQLite |
| Frontend | Vanilla JavaScript + Bootstrap 5 + Chart.js |
| Auth | Django Session Authentication |
| Config | python-dotenv |

---

## ⚙️ Installation & Setup
```bash
# 1. Clone the repository
git clone https://github.com/your-username/Study-Planner.git
cd Study-Planner/studyplanner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DEBUG=True" >> .env

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Visit `http://localhost:8000` and login with your superuser credentials.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/subjects/` | List all subjects |
| POST | `/api/subjects/` | Create a new subject |
| POST | `/api/generate/` | Generate priority-weighted timetable |
| GET | `/api/sessions/` | List all study sessions |
| PATCH | `/api/sessions/<id>/complete/` | Mark session as completed |
| GET | `/api/progress/` | Overall progress stats |
| GET | `/api/progress/daily/` | Progress grouped by date |

---

## 🧠 Algorithm

The timetable generator uses a **priority-weighted scheduling algorithm**:
```
priority_score = difficulty_weight × concentration_factor

concentration_factor:
  - Final 3 days before exam → 1.5x (50% boost)
  - Final 7 days before exam → 1.2x (20% boost)
  - Normal days             → 1.0x

difficulty_weight:
  - Easy   → 1.0x
  - Medium → 2.0x
  - Hard   → 3.5x
```

Subjects with closer exam dates are assigned **earlier time slots** each day, ensuring the most urgent work happens when focus is highest.

---

## 🗃️ Entity Relationship Diagram
```
User
 └── Subject (name, exam_date, difficulty, syllabus_completion)
      └── StudySession (date, hours_allocated, completed, notes)
```

---

## 🧪 Running Tests
```bash
python manage.py test planner
```

---

## 📁 Project Structure
```
studyplanner/
├── manage.py
├── requirements.txt
├── .env
├── planner/
│   ├── models.py        # Subject, StudySession
│   ├── serializers.py   # DRF Serializers
│   ├── views.py         # Thin API views
│   ├── services.py      # Timetable algorithm (core logic)
│   ├── urls.py          # API routes
│   └── tests.py         # Unit tests
├── studyplanner/
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── index.html
│   └── login.html
└── static/
    ├── css/style.css
    └── js/script.js
```

---

## 👨‍💻 Author

Built by **Yash Taksale** as an MNC Internship-worthy Django project.
