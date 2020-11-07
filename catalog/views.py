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
                group = student_group["name"]
                group_courses = student_group["courses"]
                for course in group_courses:
                    random_lecturer = get_random_lecturer(lecturers)
                    class_group = [group, course, random_lecturer, 6]
                    class_groups.append(class_group)

            rooms = []
            for classroom in classrooms:
                rooms.append(classroom["name"])

            schedule_t = Scheduler(rooms, class_groups)

            context = extract_context(schedule_t.timeTable)
            context = matrix_tt(context)  # sherry
            # print(context)
            return render(request, 'timetable.html', context=context)
    return render(request, 'index.html')
