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


def get_random_lecturer(lecturer_set):
    total_lecturer = len(lecturer_set)
    random_pos = random.randint(0, total_lecturer - 1)
    return lecturer_set[random_pos].name


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


@csrf_exempt
def schedule(request):

    course_set = Course.objects.all()
    lecturer_set = Lecturer.objects.all()
    classroom_set = Classroom.objects.all()
    student_group_set = StudentGroup.objects.all()

    class_groups = []

    for student_group in student_group_set:
        group = [student_group.name, student_group.strength]

        for course in student_group.courses.all():
            random_lecturer = get_random_lecturer(lecturer_set)
            class_group = [group, course.name, random_lecturer, 3]
            class_groups.append(class_group)

    rooms = []
    for classroom in classroom_set:
        cl = dict()
        cl['name'] = classroom.name
        cl['capacity'] = classroom.capacity
        rooms.append(cl)
        # rooms.append(classroom)

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
            expertise = response.POST.get("expertise")
            max_teaching_load = response.POST.get("max_teaching_load")

            Lecturer.objects.create(name=name, expertise=expertise, max_teaching_load=max_teaching_load)

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
        print(response.POST)
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
