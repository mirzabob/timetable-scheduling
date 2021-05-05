from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.courses, name="courses"),
    path('lecturers/', views.lecturers, name="courses"),
    path('classrooms/', views.classrooms, name="classrooms"),
    path('studentGroups/', views.studentGroups, name="studentGroups"),
    path('clear/', views.clear, name="clear"),
    path('schedule/', views.schedule, name="schedule")
]