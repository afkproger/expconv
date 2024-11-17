from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from questionnaire.models import Tasks, Indicators, Scale, User, ExpertsResponses


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'email', 'last_name', 'tel')


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'tel', 'email')


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ('id', 'grade', 'weight')


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = ('indicator', 'question')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description')


class TaskDetailSerializer(serializers.ModelSerializer):
    scale = ScaleSerializer(many=True, read_only=True)
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description', 'scale', 'indicators')


class UserTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'tasks')


class ExpertsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertsResponses
        fields = ('name', 'expert_token')


class ExpertQuestionnaireSerializer(serializers.ModelSerializer):
    experts_responses = ExpertsCreateSerializer(many=True, read_only=True)
    scale = ScaleSerializer(many=True, read_only=True)
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description', 'scale', 'indicators', 'experts_responses')
