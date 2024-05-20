from django.contrib import admin
from .models import Student, Semester, Course, Lecturer, Class, StudentEnrollment

# Register your models here.
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Lecturer)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(StudentEnrollment)