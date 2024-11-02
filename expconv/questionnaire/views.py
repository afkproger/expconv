from pickle import FALSE

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from questionnaire.models import Tasks, Indicators
from questionnaire.serializers import *


# тут мы можем создать , получить , обработать таски и создать его
class TaskDetailViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = (IsAuthenticated,)

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


# пролучаем настройки такска для конкретного пользователя(в самом базовом варианте написаны)
class TaskQuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserQuestionnaireSerializer


class Test(APIView):
    def post(self, request):
        user = request.user
        return Response(UserSerializer(user).data)
