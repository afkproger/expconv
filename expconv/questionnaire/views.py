from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from questionnaire.models import DecisionMakers, Tasks, Indicators
from questionnaire.serializers import *


class DecisionMakersRegistration(generics.ListCreateAPIView):
    queryset = DecisionMakers.objects.all()
    serializer_class = DecisionMakersRegistrationSerializers


class DecisionMakersViews(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        try:
            des_makers = DecisionMakers.objects.get(login=login, password=password)
            des_makers_serial = DecisionMakersSerializers(des_makers).data
            return Response(des_makers_serial)
        except DecisionMakers.DoesNotExist:
            # Если пользователь не найден
            return Response({'error': 'Пользователь не найден'}, status=404)
        except DecisionMakers.MultipleObjectsReturned:
            return Response({'error': 'Найдено несколько пользователей с этими данными. Обратитесь в поддержку.'},
                            status=400)


# view для создание таска ( т.е настройки опросника)
class TaskCreateView(APIView):
    def post(self, request):
        dm_id = request.data.get('dm_id')
        name = request.data.get('name')
        description = request.data.get('description')
        scale = request.data.get('scale')  # Получаем массив scale
        values = request.data.get('values')  # Получаем массив values

        try:
            # Находим пользователя
            dm = DecisionMakers.objects.get(pk=dm_id)

            # Создаём задачу
            task = Tasks.objects.create(name=name, description=description, decision_maker=dm)

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

            return Response(TaskCreateSerializers(task).data)

        except DecisionMakers.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)


# вывести тут все созданные опросники
class TaskDetailView(APIView):
    def post(self, request):
        dm_id = request.data.get('dm_id')
        try:
            tasks = Tasks.objects.filter(decision_maker=dm_id)
            if not tasks.exists():
                return Response({'error': 'Невозможно получить список задач для этого пользователя'}, status=404)

            return Response(TaskDetailSerializer(tasks, many=True).data)
        except DecisionMakers.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)


# вывводим информацию для формирования опросника
class TaskQuestionnaireView(APIView):
    def post(self, request):
        task_id = request.data.get('task_id')
        dm_id = request.data.get('dm_id')
        try:
            des_mak = DecisionMakers.objects.get(id=dm_id)
            task = Tasks.objects.get(pk=task_id, decision_maker_id=des_mak)
            return Response(TaskQuestionnaireSerializer(task).data)
        except Tasks.DoesNotExist:
            return Response({'error': 'Невозможно получить данные о задании'}, status=404)
