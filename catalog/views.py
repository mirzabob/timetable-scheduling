import json
import random

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

# importing scheduler class
from .Scheduler import Scheduler

# importing custom forms
from .forms import Input

# importing models
from .models import Course, Classroom, Lecturer, StudentGroup


def extract_context(timeTable):
    context = dict()
    for x in timeTable:
        day = x[0]
        room = x[1]
        timeslot = x[2]
        group = x[3]
        # print(group)
        if group[0][0] in context:
            context[group[0][0]].append([day, room, timeslot, group[1], group[2]])
        else:
            context[group[0][0]] = [[day, room, timeslot, group[1], group[2]]]
    return context


def matrix_tt(context):  # sherry_fn
    matr = dict()
    for x in context:
        matrix = []
        rows, cols = (5, 8)
        for r in range(0, rows):
            matrix.append(["0" for c in range(0, cols)])
        for y in context[x]:
            day = int(y[0])
            period = int(y[2])
            stri = y[3] + "/" + y[4] + "(" + str(y[1]) + ")"
            matrix[day][period] = stri
        matr[x] = matrix
    return matr


def get_class_group(student_group, lecturer_set):
    subject_map = {}
    lecturer_count = {}
    for lecturer in lecturer_set:
        lecturer_count[lecturer.name] = 0
        for subject in lecturer.expertise.all():
            if subject in subject_map:
                subject_map[subject].append(lecturer.name)
            else:
                subject_map[subject] = [lecturer.name]
    class_group = []
    for group in student_group:
        g = [group.name, group.strength]
        for course in group.courses.all():
            probable_lecturer = subject_map[course]
            probable_lecturer.sort(key=lambda x: lecturer_count[x])
            current_lecturer = probable_lecturer[0]
            lecturer_count[current_lecturer] += 1
            class_group.append([g, course.name, current_lecturer, 3])
    return class_group


@csrf_exempt
def schedule(request):
    course_set = Course.objects.all()
    lecturer_set = Lecturer.objects.all()
    classroom_set = Classroom.objects.all()
    student_group_set = StudentGroup.objects.all()

    rooms = []
    for classroom in classroom_set:
        cl = dict()
        cl['name'] = classroom.name
        cl['capacity'] = classroom.capacity
        rooms.append(cl)
        # rooms.append(classroom)

    class_groups = get_class_group(student_group=student_group_set, lecturer_set=lecturer_set)
    schedule_t = Scheduler(rooms, class_groups)
    ## if schedule_t.find_hard_constrain_weight(schedule_t.timeTable) >0 :
    ## could not generate time table

    context = extract_context(schedule_t.timeTable)
    context = matrix_tt(context)  # sherry
    # print(context)
    return render(request, 'timetable.html', {"context": context})


def courses(response):
    if response.method == "POST":
        if response.POST.get("delete"):
            for course in Course.objects.all():
                if response.POST.get("c" + str(course.name)) == "clicked":
                    Course.objects.filter(name=course.name).delete()

        elif response.POST.get("newItem"):
            name = response.POST.get("name")
            credit = response.POST.get("credit")
            course_year = response.POST.get("course_year")

            Course.objects.create(name=name, credit=credit, course_year=course_year)

    course_set = Course.objects.all()

    return render(response, "courses.html", {"course_set": course_set})


def lecturers(response):
    if response.method == "POST":
        if response.POST.get("delete"):
            for lecturer in Lecturer.objects.all():
                if response.POST.get("c" + str(lecturer.name)) == "clicked":
                    Lecturer.objects.filter(name=lecturer.name).delete()

        elif response.POST.get("newItem"):
            name = response.POST.get("name")
            max_teaching_load = response.POST.get("max_teaching_load")
            Lecturer.objects.create(name=name, max_teaching_load=max_teaching_load)

        elif response.POST.get("newCourse"):
            courses_input = response.POST.getlist("course")
            print(courses_input)
            course = ''
            for c in courses_input:
                if len(c):
                    course = c
                    break
            print(course)
            for lecturer in Lecturer.objects.all():
                print(lecturer)
                if response.POST.get('newCourse') == lecturer.name:
                    print(Course.objects.filter(name=course))
                    lecturer.expertise.add(Course.objects.get(name=course))

    lecturer_set = Lecturer.objects.all()

    return render(response, "lecturers.html", {"lecturer_set": lecturer_set})


def classrooms(response):
    if response.method == "POST":
        if response.POST.get("delete"):
            for classroom in Classroom.objects.all():
                if response.POST.get("c" + str(classroom.name)) == "clicked":
                    Classroom.objects.filter(name=classroom.name).delete()

        elif response.POST.get("newItem"):
            name = response.POST.get("name")
            capacity = response.POST.get("capacity")

            Classroom.objects.create(name=name, capacity=capacity)

    classroom_set = Classroom.objects.all()

    return render(response, "classrooms.html", {"classroom_set": classroom_set})


def studentGroups(response):
    if response.method == "POST":
        if response.POST.get("delete"):
            for studentGroup in StudentGroup.objects.all():
                if response.POST.get("c" + str(studentGroup.name)) == "clicked":
                    StudentGroup.objects.filter(name=studentGroup.name).delete()

        elif response.POST.get("newItem"):
            name = response.POST.get("name")
            strength = response.POST.get("strength")
            StudentGroup.objects.create(name=name, strength=strength)

        elif response.POST.get("newCourse"):
            courses_input = response.POST.getlist("course")
            print(courses_input)
            course = ''
            for c in courses_input:
                if len(c):
                    course = c
                    break
            print(course)
            for studentGroup in StudentGroup.objects.all():
                print(studentGroup)
                if response.POST.get('newCourse') == studentGroup.name:
                    print(Course.objects.filter(name=course))
                    studentGroup.courses.add(Course.objects.get(name=course))

    studentGroup_set = StudentGroup.objects.all()
    # print(studentGroups)
    return render(response, "studentGroups.html", {"studentGroup_set": studentGroup_set})


def clear(response):
    Course.objects.all().delete()
    Lecturer.objects.all().delete()
    Classroom.objects.all().delete()
    StudentGroup.objects.all().delete()

    return render(response, "clear.html", {})
