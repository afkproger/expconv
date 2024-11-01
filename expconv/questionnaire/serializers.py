from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from questionnaire.models import Tasks, Indicators, Scale, User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'fio')


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'fio')


class TaskCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'name')


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ('id', 'grade', 'weight')


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = ('indicator', 'question')


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description')


class UserQuestionnaireSerializer(serializers.ModelSerializer):
    tasks = TaskDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('tasks', 'username')

class TaskQuestionnaireSerializer(serializers.ModelSerializer):
    scale = ScaleSerializer(many=True , read_only=True)
    indicators = IndicatorSerializer(many=True , read_only=True)
    class Meta:
        model = Tasks
        fields = ()