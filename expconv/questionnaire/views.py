from pickle import FALSE
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from questionnaire.conv.EffectivenessCalculator_class import EffectivenessCalculator
from questionnaire.models import Tasks, Indicators, ExpertsResponses
from questionnaire.serializers import *


# тут мы можем создать , получить , обработать таски и создать его
# стоит изменить values на indicators
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
    serializer_class = ExpertQuestionnaireSerializer
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

    # TODO: Попробовать убрать перезапуск страницы для отображения результатов
    @action(methods=['post'], detail=False)
    def choice_experts(self, request):
        try:
            # Получаем данные из запроса
            experts = request.data.get('experts')
            task_id = request.data.get('task_id')

            if not experts or not isinstance(experts, list):
                return Response({'error': 'Invalid or missing "experts" data'}, status=status.HTTP_400_BAD_REQUEST)

            if not task_id:
                return Response({'error': 'Missing "task_id"'}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем существование задачи
            try:
                task_ = Tasks.objects.get(id=task_id)
            except Tasks.DoesNotExist:
                return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

            # Создаем ответы экспертов
            response = []
            for expert in experts:
                name = expert.get('expert_name')
                weight = expert.get('opinion_weight')

                if not name or weight is None:
                    return Response(
                        {'error': 'Each expert must have "expert_name" and "opinion_weight"'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                expert_data = ExpertsResponses.objects.create(
                    task=task_,
                    name=name,
                    opinion_weight=weight
                )
                response.append(expert_data)

            # Возвращаем сериализованные данные
            return Response(ExpertsCreateSerializer(response, many=True).data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ShowUserInfo(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class FindConvolution(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            answers = request.data.get('answers', [])
            survey_results = {}

            for answer in answers:
                index = answer.get('index')
                weight = answer.get('weight')

                if index is not None and weight is not None:
                    survey_results[index] = weight
            calculate = EffectivenessCalculator(survey_results)
            parameters_list = calculate.get_parameters_list()
            fn_labels = calculate.get_fn_labels()
            str_result = f"jрез = {EffectivenessCalculator.form_polynomial(parameters_list, fn_labels)}"

            return Response({'conv': str_result, 'list': parameters_list})

        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class CalculateConvolution(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        parameters_list = request.data.get('parameters_list')
        users_choices = request.data.get('users_choices')
        try:
            if (parameters_list is not None) and (users_choices is not None):
                answers = [float(x) for x in users_choices]
                return Response(
                    {'calculate_conv': round(EffectivenessCalculator.calculate_polynomial(parameters_list, answers),
                                             4)})
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ExpertAnswerView(APIView):
    def get(self, request):
        try:
            task = self.get_object()
            return Response(TaskDetailSerializer(task).data)
        except Tasks.DoesNotExist:
            return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        expert_token = request.query_params.get('token')


    def get_queryset(self):
        return Tasks.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        task_id = self.request.query_params.get('task')
        try:
            return queryset.get(id=task_id)
        except Exception:
            return Tasks.objects.none()
