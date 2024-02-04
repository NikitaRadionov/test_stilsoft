from rest_framework import serializers
from .models import Section, UserSection

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("title", "teacher")

class UserSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSection
        fields = ("student", "section", "date")