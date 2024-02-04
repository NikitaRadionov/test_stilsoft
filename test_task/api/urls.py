from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('sections/get', GetSectionsAPIView.as_view()),
    path('sections/create', CreateSectionAPIView.as_view()),
    path('sections/delete', DeleteSectionAPIView.as_view()),
    path('sections/section/getStudents', GetSectionStudentsAPIView.as_view()),
    path('student/joinSection', JoinSectionAPIView.as_view()),
    path('student/leaveSection', LeaveSectionAPIView.as_view()),
    path('student/getMySections', GetStudentSectionsAPIView.as_view()),
    path('teacher/leadSection', LeadSectionAPIView.as_view()),
    path('teacher/leaveSection', UnleadSectionAPIView.as_view()),
]