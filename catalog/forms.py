from django import forms
import json
from jsonschema import validate

schema_course = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "credit": {"type": "number"},
            "course_year": {"type": "number"}
        }
    },
}

schema_lecturer = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "expertise": {"type": "string"},
            "max_teaching_load": {"type": "number"}
        }
    },
}

schema_classroom = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "capacity": {"type": "number"}
        }
    },
}

schema_studentgroup = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "strength": {"type": "number"},
            "courses": {"type": "array"}
        }
    },
}


class Input(forms.Form):
    course = forms.CharField(max_length=10000)
    lecturer = forms.CharField(max_length=10000)
    classroom = forms.CharField(max_length=10000)
    studentgroup = forms.CharField(max_length=10000)

    def clean_jsonfield(self):
        courses = self.cleaned_data['course']
        lecturers = self.cleaned_data['lecturer']
        classrooms = self.cleaned_data['classroom']
        studentgroup = self.cleaned_data['studentgroup']

        try:
            courses = json.loads(courses)
            lecturers = json.loads(lecturers)
            classrooms = json.loads(classrooms)
            studentgroup = json.loads(studentgroup)

            validate(instance=courses, schema=schema_course)
            validate(instance=lecturers, schema=schema_lecturer)
            validate(instance=classrooms, schema=schema_classroom)
            validate(instance=studentgroup, schema=schema_studentgroup)

        except:
            raise forms.ValidationError("Invalid data in JSON Format")

        return courses, lecturers, classrooms, studentgroup
