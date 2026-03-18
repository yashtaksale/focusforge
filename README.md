# 🔥 FocusForge — AI Smart Study Planner

> **Build Discipline. Eliminate Distractions. Execute Consistently.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/DRF-3.15-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/AI-TensorFlow.js-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

---

## 🚀 Live Preview (Coming Soon)

> 🌐 Deployment in progress (Render / AWS)

---

## 🧠 What is FocusForge?

Most students don’t fail because they lack knowledge —
they fail because of **poor planning + distractions**.

**FocusForge** is a production-grade AI-powered study planner that:

* Generates **priority-based timetables**
* Tracks **real-time study progress**
* Uses **AI-powered phone detection** to eliminate distractions

> ⚡ This is not just a planner — it's a **discipline engine**

---

## 🖼 Screenshots

>

###  Dashboard

<img width="1919" height="1079" alt="Dashboard" src="https://github.com/user-attachments/assets/f10111b6-950a-4c08-bdb4-c6edd97c86a0" />


###  Deep Focus Mode

https://github.com/user-attachments/assets/b1ad0ed7-758e-4e51-9f1d-96880af3dce5


### 📅 Generated Timetable

<img width="1919" height="1079" alt="Generated Timetable" src="https://github.com/user-attachments/assets/9424197b-e572-48ad-91fc-242eda8e9cc5" />


---

## ✨ Key Features

### 📅 Smart Scheduling Engine

Automatically generates optimized study schedules based on:

* Subject difficulty
* Exam deadlines
* Available study hours

---

### ⚡ Priority-Weighted Algorithm

```python
priority_score = difficulty_weight × time_sensitivity_factor
```

Ensures:

* Hard + urgent subjects → more time
* Easy + distant subjects → balanced scheduling

---

### 🔴 Deep Focus Mode (AI Powered)

* 📷 Webcam-based **phone detection**
* 🚨 Real-time distraction alerts
* ⏱ Session timer + distraction counter

---

### 📊 Progress Dashboard

* Visual charts (Chart.js)
* Subject-wise completion tracking
* Daily productivity insights

---

### 🔔 Smart Notifications

* Reminders at:

  * 30 min
  * 10 min
  * 5 min
  * Session start

---

### 🔐 Secure Authentication

* Django session-based auth
* Per-user data isolation

---

## 🛠 Tech Stack

| Layer    | Technology               |
| -------- | ------------------------ |
| Backend  | Django 6.0 + DRF         |
| Frontend | HTML, CSS, JavaScript    |
| Database | SQLite / PostgreSQL      |
| AI       | TensorFlow.js + COCO-SSD |
| Charts   | Chart.js                 |

---

## 🏗 Architecture

```
Frontend (Browser)
        ↓
Django REST API
        ↓
Service Layer (Algorithm)
        ↓
Database
```

> Clean, scalable, and production-ready architecture

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/focusforge.git
cd focusforge/studyplanner

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 📁 Project Structure

```
planner/        → core logic
services.py     → scheduling algorithm
templates/      → frontend UI
static/         → CSS & JS
```

---

## 🗺 Roadmap

* [x] AI-based timetable generation
* [x] Deep Focus Mode
* [x] Progress tracking
* [x] Notifications
* [ ] Mobile App (React Native)
* [ ] Cloud Deployment
* [ ] AI Recommendations

---

## 👨‍💻 Author

**Yash Taksale**
Computer Science Engineering Student

---

## ⭐ Support

If you found this useful:
👉 Star this repo
👉 Share with friends

> Discipline beats motivation. FocusForge builds discipline.
