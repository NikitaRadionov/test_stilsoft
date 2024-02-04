from django.shortcuts import render
from django.db.models import Q
from .serializers import SectionSerializer, UserSectionSerializer
from .models import ApiUser, Section, UserSection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

# Create your views here.

class CreateSectionAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        title = request.data['title']
        user = request.user

        data = {
            "success": False
        }

        if (user.role == "MODERATOR" or user.role == "TEACHER"):
            if (len(Section.objects.filter(title=title))):
                data["error"]= {
                    "code": 400,
                    "message": "Section already exists"
                    }
            else:
                section = Section.objects.create(title=title)
                data["success"] = True
                data["data"] = SectionSerializer(section).data
        else:
            data["error"] = {
                "code": 403,
                "message": "Only Teacher or Moderator can create sections"
                }

        return Response(data)


class GetSectionsAPIView(ListAPIView):

    permission_classes = (IsAuthenticated, )
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'title', 'teacher']


class DeleteSectionAPIView(DestroyAPIView):

    permission_classes = (IsAuthenticated, )

    def delete(self, request):

        title = request.data['title']
        user = request.user

        data = {
            "success": False
        }

        if (user.role == "MODERATOR"):
            try:
                section = Section.objects.get(title=title)
                section.delete()
                data["success"] = True
                data["data"] = {"message": "Success section delete"}
            except Section.DoesNotExist:
                data["error"] = {
                    "code": 400,
                    "message": "Section does not exists"
                    }
        else:
            data["error"] = {
                "code": 403,
                "message": "Only Moderator can delete sections"
                }

        return Response(data)


class JoinSectionAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):

        title = request.data['title']
        user = request.user

        data = {
            "success": False
        }

        if (user.role == "STUDENT"):
            try:
                section = Section.objects.get(title=title)
                try:
                    userSection = UserSection.objects.get(student=user, section=section)
                    data["error"] = {
                        "code": 400,
                        "message": "Student already joined this section"
                        }
                except UserSection.DoesNotExist:
                    userSection = UserSection.objects.create(student=user, section=section)
                    data["success"] = True
                    data["data"] = UserSectionSerializer(userSection).data
            except Section.DoesNotExist:
                data["error"] = {
                    "code": 400,
                    "message": "Section does not exists"
                    }
        else:
            data["error"] = {
                "code": 403,
                "message": "Only Student can join section"
                }

        return Response(data)


class LeaveSectionAPIView(DestroyAPIView):

    permission_classes = (IsAuthenticated, )

    def delete(self, request):

        title = request.data['title']
        user = request.user

        data = {
            "success": False
        }

        if (user.role == "STUDENT"):
            try:
                section = Section.objects.get(title=title)
                try:
                    userSection = UserSection.objects.get(student=user, section=section)
                    userSection.delete()
                    data["success"] = True
                    data["data"] = {
                        "message": "Success leave section"
                        }
                except UserSection.DoesNotExist:
                    data["error"] = {
                        "code": 400,
                        "message": "Student is not member of this section"
                        }
            except Section.DoesNotExist:
                data["error"] = {
                    "code": 400,
                    "message": "Section does not exists"
                    }
        else:
            data["error"] = {
                "code": 403,
                "message": "Only Student can leave section"
                }

        return Response(data)


class LeadSectionAPIView(UpdateAPIView):

    permission_classes = (IsAuthenticated, )

    def patch(self, request):

        title = request.data['title']
        user = request.user

        data = {
            "success": False
        }

        if (user.role == "TEACHER"):
            try:
                section = Section.objects.get(title=title)
                if section.teacher is None:
                    data["error"] = {
                        "code": 400,
                        "message": "Section already have teacher"
                        }
                else:
                    section.update(teacher=user)
                    data["success"] = True
                    data["data"] = SectionSerializer(section).data
            except Section.DoesNotExist:
                data["error"] = {
                    "code": 400,
                    "message": "Section does not exists"
                    }
        else:
            data["error"] = {
                "code": 403,
                "message": "Only Teacher can lead section"
                }

        return Response(data)


class UnleadSectionAPIView(UpdateAPIView):

    permission_classes = (IsAuthenticated, )

    def patch(self, request):

        title = request.data['title']
        user = request.user

        data = {
            "success": False,
        }

        if (user.role == "TEACHER"):
            try:
                section = Section.objects.get(title=title)
                if section.teacher is None:
                    data["error"] = {
                        "code": 400,
                        "message": "Section haven't teacher"
                        }
                else:
                    section.update(teacher=None)
                    data["success"] = True
                    data["data"] = data = SectionSerializer(section).data
            except Section.DoesNotExist:
                data["error"] = {
                        "code": 400,
                        "message": "Section does not exists"
                }
        else:
            data["error"] = {
                "code": 403,
                "message": "Only Teacher can leave teacher section position"
            }

        return Response(data)


class GetSectionStudentsAPIView(ListAPIView):

    permission_classes = (IsAuthenticated, )
    queryset = UserSection.objects.all()
    serializer_class = UserSectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['student', 'section']


class GetStudentSectionsAPIView(ListAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = UserSectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['student', 'section']

    def get_queryset(self):
        user = self.request.user
        queryset = UserSection.objects.filter(student=user)
        return queryset
