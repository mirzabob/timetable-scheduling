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
from .models import Course, Classroom, Lecturer, Class, StudentGroup


def get_random_lecturer(lecturers):
    total_lecturer = len(lecturers)
    random_pos = random.randint(0, total_lecturer - 1)
    return lecturers[random_pos]["name"]


def extract_context(timeTable):
    context = dict()
    for x in timeTable:
        day = x[0]
        room = x[1]
        timeslot = x[2]
        group = x[3]
        if group[0] in context:
            context[group[0]].append([day, room, timeslot, group[1], group[2]])
        else:
            context[group[0]] = [[day, room, timeslot, group[1], group[2]]]
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
            stri = y[3] + "/" + y[4] + "(" + y[1] + ")"
            matrix[day][period] = stri
        matr[x] = matrix
    return matr


@csrf_exempt
def schedule(request):
    if request.method == 'POST':
        input_data = Input(request.POST)
        if input_data.is_valid():
            courses, lecturers, classrooms, student_groups = input_data.clean_jsonfield()

            class_groups = []

            for student_group in student_groups:
                group = [student_group["name"], int(student_group["strength"])]
                group_courses = student_group["courses"]
                for course in group_courses:
                    random_lecturer = get_random_lecturer(lecturers)
                    class_group = [group, course, random_lecturer, 3]
                    class_groups.append(class_group)

            rooms = []
            for classroom in classrooms:
                rooms.append(classroom)

            schedule_t = Scheduler(rooms, class_groups)
            ## if schedule_t.find_hard_constrain_weight(schedule_t.timeTable) >0 :
            ##   could notr generate time table

            context = extract_context(schedule_t.timeTable)
            context = matrix_tt(context)  # sherry
            # print(context)
            return render(request, 'timetable.html', context=context)
    return render(request, 'index.html')


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

        # elif response.POST.get("newCourse"):
        #     print("OK")
        #     course = response.POST.get("course")
        #     print(course)
        #     for studentGroup in StudentGroup.objects.all():
        #         if response.POST.get("c" + str(studentGroup.name)) == "newCourse":
        #             StudentGroup.objects.filter(name=studentGroup.name).coursestaken_set.create(course_name=course)

    studentGroup_set = StudentGroup.objects.all()

    return render(response, "studentGroups.html", {"studentGroup_set": studentGroup_set})


def clear(response):

    Course.objects.all().delete()
    Lecturer.objects.all().delete()
    Classroom.objects.all().delete()
    StudentGroup.objects.all().delete()

    return render(response, "clear.html", {})