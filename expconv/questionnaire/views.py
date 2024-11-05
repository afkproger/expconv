from pickle import FALSE

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from questionnaire.models import Tasks, Indicators
from questionnaire.serializers import *


# тут мы можем создать , получить , обработать таски и создать его
class TaskDetailViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(methods=['post'], detail=False)
    def createtask(self, request):
        user = request.user
        name = request.data.get('name')
        description = request.data.get('description')
        scale = request.data.get('scale')  # Получаем массив scale
        values = request.data.get('values')  # Получаем массив values

        try:
            # Находим пользователя

            # Создаём задачу
            task = Tasks.objects.create(name=name, description=description, user=user)

            # Обрабатываем значения из массива scale
            for item in scale:
                grade = item.get('grade')
                weight = item.get('weight')

                # Создаём связанные объекты Scale
                Scale.objects.create(
                    task=task,  # Связь с задачей
                    grade=grade,
                    weight=weight
                )

            # Обрабатываем значения из массива values
            for value in values:
                indicator = value.get('indicators')
                question = value.get('question')

                # Создаём связанные объекты Indicators
                Indicators.objects.create(
                    task=task,  # Связь с задачей
                    indicator=indicator,
                    question=question
                )

            return Response(TaskSerializer(task).data)

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)


# пролучаем настройки таска для конкретного пользователя
class TaskQuestionnaireViewSet(viewsets.ModelViewSet):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем пустой QuerySet, если pk не указан
        task_id = self.kwargs.get('pk')
        if task_id is None:
            return Tasks.objects.none()  # Пустой QuerySet

        # Если pk указан, возвращаем только задачи текущего пользователя
        return Tasks.objects.filter(user=self.request.user)

    def get_object(self):
        # Пытаемся найти задачу по `id`
        task_id = self.kwargs.get('pk')

        if task_id is None:
            raise NotFound({'error': 'Не указан id задачи'})

        try:
            task = self.get_queryset().get(id=task_id)
        except Tasks.DoesNotExist:
            raise NotFound({'error': 'Задача не найдена'})

        return task


class ShowUserInfo(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
