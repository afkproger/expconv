from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    tel = models.CharField(max_length=15, blank=True, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email','tel' ]

    def __str__(self):
        return self.username


class Tasks(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name


class Scale(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='scale')
    grade = models.CharField(max_length=255)
    weight = models.FloatField()

    def __str__(self):
        return f'{self.grade} - {self.weight}'


class Indicators(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='indicators')
    indicator = models.CharField(max_length=255)
    question = models.TextField()

    def __str__(self):
        return f'{self.indicator} - {self.question}'
