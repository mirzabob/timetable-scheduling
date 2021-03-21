from django.db import models


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    credit = models.IntegerField(default=0)
    course_year = models.IntegerField()


class Lecturer(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    expertise = models.CharField(max_length=50)
    max_teaching_load = models.IntegerField(default=999999999)


class Classroom(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    capacity = models.IntegerField(default=99999999)


class StudentGroup(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    strength = models.IntegerField(default=0)


class Class(models.Model):
    student_group = models.ForeignKey(StudentGroup, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    lecturers = models.ForeignKey(Lecturer, on_delete=models.PROTECT)


# class Enrolled(models.Model):
#     student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
#     course_name = models.CharField(max_length=50)
