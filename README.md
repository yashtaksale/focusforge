<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=FocusForge&fontSize=80&fontColor=fff&animation=twinkling&fontAlignY=35&desc=AI%20Smart%20Study%20Planner&descAlignY=60&descSize=22" width="100%"/>

<br/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Nunito&weight=800&size=22&pause=1000&color=FF6B6B&center=true&vCenter=true&width=600&lines=Build+Discipline.+Eliminate+Distractions.;AI-Powered+Priority+Scheduling.;Deep+Focus+Mode+with+Phone+Detection.;Execute+Consistently.+Every+Day.)](https://git.io/typing-svg)

<br/>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/REST_Framework-3.15-DC143C?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/TensorFlow.js-AI_Detection-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/Chart.js-Progress_Viz-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-52D9A6?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/github/stars/yashtaksale/focusforge?style=social"/>
  &nbsp;
  <img src="https://img.shields.io/github/forks/yashtaksale/focusforge?style=social"/>
  &nbsp;
  <img src="https://img.shields.io/github/watchers/yashtaksale/focusforge?style=social"/>
</p>

</div>

---

## 🧠 What Problem Does This Solve?

<table>
<tr>
<td width="50%">

### ❌ Before FocusForge
- Students plan randomly with no priority logic
- Hard subjects get equal time as easy ones
- No tracking → no accountability
- Phone distractions silently kill study sessions
- Exam panic from poor time management

</td>
<td width="50%">

### ✅ After FocusForge
- AI generates a **priority-weighted** timetable
- Difficult subjects automatically get more time
- Real-time progress tracking with visual charts
- AI detects phone usage and alerts you instantly
- Calm, structured, deadline-aware scheduling

</td>
</tr>
</table>

> **💡 Core Insight:** Students don't fail from lack of knowledge — they fail from poor planning and constant distractions. FocusForge solves both.

---

## 🖼️ Screenshots

### 🏠 Dashboard — Add Subjects & Track Progress
<img width="1919" height="1079" alt="Dashboard" src="https://github.com/user-attachments/assets/f10111b6-950a-4c08-bdb4-c6edd97c86a0"/>

<br/>

### 🔴 Deep Focus Mode — AI Phone Detection Live
https://github.com/user-attachments/assets/b1ad0ed7-758e-4e51-9f1d-96880af3dce5

<br/>

### 📅 Generated Timetable — Priority-Weighted Sessions
<img width="1919" height="1079" alt="Generated Timetable" src="https://github.com/user-attachments/assets/9424197b-e572-48ad-91fc-242eda8e9cc5"/>

---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 📅 Smart Scheduling Engine
Generates a full study timetable based on subject difficulty, exam dates, and your available hours. Every session includes a specific time slot, study approach, and step-by-step actions.

### 🔴 Deep Focus Mode *(Most Unique Feature)*
A dedicated focus page powered by **TensorFlow.js + COCO-SSD**. The AI watches through your webcam and detects phone usage in real time. Get caught → instant alert. A distraction counter tracks every lapse.

### ⚡ Priority-Weighted Algorithm
Not all subjects deserve equal time. The engine computes a `priority_score` per subject and allocates sessions accordingly — urgent + difficult subjects always come first.

</td>
<td width="50%" valign="top">

### 📊 Progress Dashboard
Visual doughnut chart with per-subject completion bars. See your overall progress percentage, completed sessions, and remaining workload at a glance.

### 🔔 Smart Study Reminders
Browser push notifications scheduled to fire at **30 min, 10 min, 5 min**, and the exact moment your session starts — so you never miss a slot.

### 🧠 Study Strategy Engine
Detects whether a subject is Coding, Mathematics, or Theory and generates a tailored learning approach — not just hours allocated, but *how* to use them effectively.

</td>
</tr>
</table>

---

## ⚡ Core Algorithm

The heart of FocusForge is its **priority-weighted scheduling engine:**

```python
priority_score = difficulty_weight × time_sensitivity_factor
```

<table>
<tr>
<td width="50%">

**📊 Difficulty Weights**

| Level | Weight | Effect |
|-------|--------|--------|
| 🟢 Easy | `1.0×` | Fewer, lighter sessions |
| 🟡 Medium | `2.0×` | Balanced allocation |
| 🔴 Hard | `3.5×` | More, intensive sessions |

</td>
<td width="50%">

**⏳ Time Sensitivity**

| Days to Exam | Multiplier | Label |
|---|---|---|
| ≤ 3 days | `1.5×` | 🚨 Critical |
| ≤ 7 days | `1.2×` | 🔥 High |
| > 7 days | `1.0×` | 📅 Normal |

</td>
</tr>
</table>

**Result:** A Hard subject with 3 days left gets `3.5 × 1.5 = 5.25×` the weight of an Easy subject with plenty of time — automatically pushed to earlier, longer, higher-priority sessions.

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=python" width="48"/><br/>
  <sub><b>Python 3.11</b></sub>
</td>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=django" width="48"/><br/>
  <sub><b>Django 6.0</b></sub>
</td>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=js" width="48"/><br/>
  <sub><b>JavaScript</b></sub>
</td>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=html" width="48"/><br/>
  <sub><b>HTML5</b></sub>
</td>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=css" width="48"/><br/>
  <sub><b>CSS3</b></sub>
</td>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=sqlite" width="48"/><br/>
  <sub><b>SQLite</b></sub>
</td>
<td align="center" width="110">
  <img src="https://skillicons.dev/icons?i=tensorflow" width="48"/><br/>
  <sub><b>TensorFlow.js</b></sub>
</td>
</tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│           Browser  (HTML / CSS / JS)        │
│    Chart.js  ·  TensorFlow.js  ·  Fetch API │
└────────────────────┬────────────────────────┘
                     │  REST API calls
┌────────────────────▼────────────────────────┐
│          Django REST Framework              │
│   Authentication  ·  Serializers  ·  Views  │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│              Service Layer                  │
│   services.py  —  Scheduling Algorithm      │
│   Priority score  ·  Time allocation        │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│             SQLite Database                 │
│         Subject  ·  StudySession            │
└─────────────────────────────────────────────┘
```

> Clean separation of concerns — the frontend is fully decoupled from the backend via REST API. Any layer can be swapped independently.

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/subjects/` | List all subjects |
| `POST` | `/api/subjects/` | Create a subject |
| `PUT` | `/api/subjects/<id>/` | Update subject details |
| `DELETE` | `/api/subjects/<id>/` | Delete a subject |
| `POST` | `/api/generate/` | Generate full timetable |
| `GET` | `/api/sessions/` | Get all study sessions |
| `PATCH` | `/api/sessions/<id>/complete/` | Mark session complete |
| `GET` | `/api/progress/` | Overall progress stats |
| `GET` | `/api/timetable/export_pdf/` | Export plan as PDF |

---

## 🗃️ Data Model

```
User
 └── Subject
      ├── name
      ├── exam_date
      ├── difficulty              (1=Easy · 2=Medium · 3=Hard)
      ├── selected_topics         (JSON array)
      ├── study_start_time
      └── study_end_time
           │
           ▼
      StudySession
        ├── date
        ├── start_time / end_time
        ├── hours_allocated
        ├── priority_label        (Critical · High · Medium · Low)
        ├── approach
        ├── technique
        ├── steps                 (JSON array)
        └── completed             (Boolean)
```

---

## ⚙️ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yashtaksale/focusforge.git
cd focusforge/studyplanner

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment setup
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DEBUG=True" >> .env

# 5. Run migrations and start server
python manage.py migrate
python manage.py runserver
```

Open **http://localhost:8000** — register an account and generate your first plan in under a minute.

---

## 📁 Project Structure

```
focusforge/
├── manage.py
├── requirements.txt
├── .env
│
├── planner/                    ← main application
│   ├── models.py               ← Subject, StudySession models
│   ├── serializers.py          ← DRF serializers
│   ├── views.py                ← API endpoints
│   ├── services.py             ← 🧠 scheduling algorithm
│   ├── urls.py
│   └── tests.py
│
├── studyplanner/               ← project configuration
│   ├── settings.py
│   └── urls.py
│
├── templates/
│   ├── index.html              ← main dashboard
│   ├── focus.html              ← deep focus mode
│   └── login.html
│
└── static/
    ├── css/style.css
    └── js/script.js
```

---

## 🗺️ Roadmap

| Status | Feature |
|--------|---------|
| ✅ Shipped | Priority-weighted timetable generation |
| ✅ Shipped | Deep Focus Mode with AI phone detection |
| ✅ Shipped | Progress dashboard with Chart.js |
| ✅ Shipped | Smart browser push notifications |
| ✅ Shipped | PDF timetable export |
| ✅ Shipped | Topic-based session scheduling |
| 🔄 Planned | Mobile app (React Native) |
| 🔄 Planned | Cloud deployment (Render / AWS) |
| 🔄 Planned | AI-powered topic recommendations |
| 🔄 Planned | Predicted exam readiness score |
| 🔄 Planned | Collaborative study rooms |

---

## 👨‍💻 Author

<table>
<tr>
<td align="center">
  <b>Yash Taksale</b><br/>
  Computer Science Engineering<br/><br/>
  <a href="https://github.com/yashtaksale">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/yashtaksale">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
</td>
</tr>
</table>

---

<div align="center">

**⭐ If FocusForge impressed you, drop a star — it takes 2 seconds and means everything.**

<br/>

> *"Discipline beats motivation. Motivation is fleeting. Systems are permanent."*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

</div>
