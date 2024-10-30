from django.db import models


class DecisionMakers(models.Model):
    fio = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.fio


class Tasks(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    decision_maker = models.ForeignKey('DecisionMakers', on_delete=models.CASCADE)

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
