from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import SemesterList, SemesterCreate, SemesterUpdate, SemesterDelete, SemesterDetail, CourseList, \
    CourseCreate, CourseUpdate, CourseDelete, CourseDetail, LecturerList, LecturerCreate, LecturerUpdate, \
    LecturerDelete, LecturerDetail, ClassList, ClassCreate, ClassUpdate, ClassDetail, ClassDelete, StudentList,  StudentCreate, StudentUpdate, StudentDetail, StudentDelete

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='student')
router.register('semesters', views.SemesterViewSet, basename='semester')
router.register('courses', views.CourseViewSet, basename='course')
router.register('lecturers', views.LecturerViewSet, basename='lecturer')
router.register('classes', views.ClassViewSet, basename='class')




urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.student_detail, name='view_student'),
    path("semester_list/", SemesterList.as_view(), name="semester_list"),
    path("semester_create/", SemesterCreate.as_view(), name="semester_create"),
    path("semester_update/<int:pk>/", SemesterUpdate.as_view(), name="semester_update"),
    path("semester_delete/<int:pk>/", SemesterDelete.as_view(), name="semester_delete"),
    path("semester_detail/<int:pk>/", SemesterDetail.as_view(), name="semester_detail"),
    path("course_list/", CourseList.as_view(), name="course_list"),
    path("course_create/", CourseCreate.as_view(), name="course_create"),
    path("course_update/<int:pk>/", CourseUpdate.as_view(), name="course_update"),
    path("course_delete/<int:pk>/", CourseDelete.as_view(), name="course_delete"),
    path("course_detail/<int:pk>/", CourseDetail.as_view(), name="course_detail"),
    path("lecturer_list/", LecturerList.as_view(), name="lecturer_list"),
    path("lecturer_create/", LecturerCreate.as_view(), name="lecturer_create"),
    path("lecturer_update/<int:pk>/", LecturerUpdate.as_view(), name="lecturer_update"),
    path("lecturer_delete/<int:pk>/", LecturerDelete.as_view(), name="lecturer_delete"),
    path("lecturer_detail/<int:pk>/", LecturerDetail.as_view(), name="lecturer_detail"),
    path("class_list/", ClassList.as_view(), name="class_list"),
    path("class_create/", ClassCreate.as_view(), name="class_create"),
    path("class_update/<int:pk>/", ClassUpdate.as_view(), name="class_update"),
    path("class_delete/<int:pk>/", ClassDelete.as_view(), name="class_delete"),
    path("class_detail/<int:pk>/", ClassDetail.as_view(), name="class_detail"),
    path("student_list/", StudentList.as_view(), name='student_list'),
    path("student_create/", StudentCreate.as_view(), name='student_create'),
    path("student_update/<int:pk>/", StudentUpdate.as_view(), name='student_update'),
    path("student_delete/<int:pk>/", StudentDelete.as_view(), name='student_delete'),
    path("student_detail/<int:pk>/", StudentDetail.as_view(), name='student_detail'),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('upload_file/', views.upload_students_excel, name='upload_file'),
    path('download_students/', views.download_students_excel, name='download_students'),
    path('send_email_out/', views.send_email, name='send_email_out'),
    path('api/', include(router.urls))

]
