from rest_framework import serializers
from .models import Section, UserSection

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("title")

class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSection
        fields = ("student", "section", "date")