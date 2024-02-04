from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ApiUser(AbstractUser):
    class Role(models.TextChoices):
        MODERATOR = "MODERATOR", 'Moderator'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'

    role = models.CharField(max_length=50, choices=Role.choices)
    REQUIRED_FIELDS = ["role"]


class Section(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(ApiUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title}'


class UserSection(models.Model):

    student = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="+")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'({self.student}, {self.section}, {self.date})'