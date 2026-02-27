from django.contrib import admin
from django.urls import path
from django.shortcuts import render

# A quick function to show your index.html
def home(request):
    # This 'tasks' list mimics what the backend will eventually send
    dummy_tasks = [
        {'name': 'Java Inheritance Lab', 'date': '2026-03-01'},
        {'name': 'Digital Footprints Poster', 'date': '2026-03-05'}
    ]
    return render(request, 'index.html', {'tasks': dummy_tasks})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home), # This makes your index.html the home page
]