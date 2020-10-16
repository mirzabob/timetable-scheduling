from django.contrib import admin

# Register your models here.
from .models import Course, Classroom, Lecturer, Class, StudentGroup
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Classroom)
admin.site.register(Lecturer)
admin.site.register(StudentGroup)


