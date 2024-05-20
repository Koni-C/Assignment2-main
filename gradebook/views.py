import csv
from datetime import datetime
import uuid
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
import pandas as pd
from django.core.mail import send_mail
from openpyxl.workbook.workbook import Workbook
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import LoginForm
from .models import Student, StudentEnrollment, Lecturer, Class, Semester, Course
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .serializer import StudentEnrollmentSerializer, UserSerializer


# Create your views here.
def index(request):
    return render(request, 'index.html', {
        'students': Student.objects.all()
    })


def student_detail(request, id):
    student = get_object_or_404(Student, pk=id)
    return render(request, 'student_list.html', {'student': student})


class SemesterList(ListView):
    model = Semester
    template_name = "Semester_List.html"


class SemesterCreate(CreateView):
    model = Semester
    template_name = "Semester_Create.html"
    fields = "__all__"
    success_url = reverse_lazy("semester_list")


class SemesterUpdate(UpdateView):
    model = Semester
    template_name = "Semester_Update.html"
    fields = "__all__"
    success_url = reverse_lazy("semester_list")


class SemesterDetail(DetailView):
    model = Semester
    template_name = "Semester_Detail.html"

class SemesterDelete(DeleteView):
    model = Semester
    template_name = "Semester_Delete.html"
    success_url = reverse_lazy("semester_list")


class CourseList(ListView):
    model = Course
    template_name = "Course_List.html"


class CourseCreate(CreateView):
    model = Course
    template_name = "Course_Create.html"
    fields = "__all__"
    success_url = reverse_lazy("course_list")


class CourseUpdate(UpdateView):
    model = Course
    template_name = "Course_Update.html"
    fields = "__all__"
    success_url = reverse_lazy("course_list")


class CourseDetail(DetailView):
    model = Course
    template_name = "Course_Detail.html"


class CourseDelete(DeleteView):
    model = Course
    template_name = "Course_Delete.html"
    success_url = reverse_lazy("course_list")


class LecturerList(ListView):
    model = Lecturer
    template_name = "Lecturer_List.html"


class LecturerCreate(CreateView):
    model = Lecturer
    template_name = "Lecturer_Create.html"
    fields = "__all__"
    success_url = reverse_lazy("lecturer_list")


class LecturerUpdate(UpdateView):
    model = Lecturer
    template_name = "Lecturer_Update.html"
    fields = "__all__"
    success_url = reverse_lazy("lecturer_list")


class LecturerDetail(DetailView):
    model = Lecturer
    template_name = "Lecturer_Detail.html"


class LecturerDelete(DeleteView):
    model = Lecturer
    template_name = "Lecturer_Delete.html"
    success_url = reverse_lazy("lecturer_list")


class ClassList(ListView):
    model = Class
    template_name = "Class_List.html"


class ClassCreate(CreateView):
    model = Class
    template_name = "Class_Create.html"
    fields = "__all__"
    success_url = reverse_lazy("class_list")


class ClassUpdate(UpdateView):
    model = Class
    template_name = "Class_Update.html"
    fields = "__all__"
    success_url = reverse_lazy("class_list")


class ClassDetail(DetailView):
    model = Class
    template_name = "Class_Detail.html"


class ClassDelete(DeleteView):
    model = Class
    template_name = "Class_Delete.html"
    success_url = reverse_lazy("class_list")


class StudentList(ListView):
    model = Student
    template_name = "Student_List.html"
    context_object_name = 'students'


class StudentCreate(CreateView):
    model = Student
    template_name = "Student_Create.html"
    fields = "__all__"
    success_url = reverse_lazy("student_list")


class StudentUpdate(UpdateView):
    model = Student
    template_name = "Student_Update.html"
    fields = "__all__"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            student_id = form.cleaned_data['student_ID']
            student_enrollment = StudentEnrollment.objects.get(student_ID=student_id)
            student_enrollment.grade = form.cleaned_data['grade']
            student_enrollment.save()
        return super().form_valid(form)


class StudentDetail(DetailView):
    model = Student
    template_name = "Student_Detail.html"


class StudentDelete(DeleteView):
    model = Student
    template_name = "Student_Delete.html"
    success_url = reverse_lazy("student_list")


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def download_students_excel(request):
    students = Student.objects.all()
    df = pd.DataFrame(list(students.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'
    df.to_excel(response, index=False)
    return response


def upload_students_excel(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'File is not in Excel format')
            return render(request, 'upload_file.html')

        df = pd.read_excel(file)
        for index, row in df.iterrows():
            student_id = int(row['Student ID'])
            first_name = str(row['First Name'])
            last_name = str(row['Last Name'])
            dob_str = str(row['DOB'])
            dob = datetime.strptime(dob_str.split(' ')[0], '%Y-%m-%d').date()
            email = str(row['email'])

            username = email
            while User.objects.filter(username=username).exists():
                username = email + '_' + str(uuid.uuid4())[:8]  # Append a unique identifier to the username

            user = User.objects.create_user(username=username, email=email)
            student = Student.objects.create(
                student_ID=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                dob=dob,
                user=user
            )

        messages.success(request, 'Students uploaded successfully')
        return render(request, 'upload_file.html')

    return render(request, 'upload_file.html')


def download_students_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.append(['Student ID', 'First Name', 'Last Name', 'DOB'])

    students = Student.objects.all()
    for student in students:
        ws.append([student.student_ID, student.first_name, student.last_name, student.dob.strftime('%Y-%m-%d')])

    wb.save(response)
    return response

def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        from_email = request.POST.get('from_email')
        to_email = request.POST.get('to_email')

        # Send email
        send_mail(subject, body, from_email, [to_email])
        email_sent = True
    else:
        email_sent = False

    return render(request, 'send_email_out.html', {'email_sent': email_sent})


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]