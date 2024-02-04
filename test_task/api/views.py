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
        # print(request.data) # <QueryDict: {'title': ['Math']}>
        # print(request.query_params) # <QueryDict: {}>
        # print(request.user) # newmoder ApiUser obj
        # print(request.auth) # 787055ed2b63edc93f18d4319e6a9415015d22bc
        # print(request.authenticators) # [<rest_framework.authentication.TokenAuthentication object at 0x0000021C0C100970>,
        # # <rest_framework.authentication.BasicAuthentication object at 0x0000021C0C1017E0>,
        # # <rest_framework.authentication.SessionAuthentication object at 0x0000021C0C101780>]
        title = request.data['title'] #
        user = request.user # ApiUser obj

        data = {
            "success": False
        }

        if (user.role == "MODERATOR" or user.role == "TEACHER"):
            if (len(Section.objects.filter(title=title))):
                # сообщение о том, что такая секция уже есть
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


# class GetSectionStudentsAPIView(ListAPIView):

#     permission_classes = (IsAuthenticated, )

#     def get(self, request):

#         title = request.data['title']
#         user = request.user

#         try:
#             section = Section.objects.get(title=title)
#             usersSection = UserSection.objects.filter(section=section)
#             data = UserSectionSerializer(usersSection).data

#         except Section.DoesNotExist:
#             data = {"message": "Section does not exists"}

#         return Response(data)


# class GetStudentSectionsAPIView(ListAPIView):

#     serializer_class = UserSection
#     permission_classes = (IsAuthenticated, )

#     def get_queryset(self):
#         user = self.request.user
#         queryset = UserSection.objects.filter(student=user)
#         return queryset
