from django.contrib import admin

# Register your models here.
from .models import Course, Classroom, Lecturer, StudentGroup
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(Lecturer)
admin.site.register(StudentGroup)


