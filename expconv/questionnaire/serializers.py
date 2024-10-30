from rest_framework import serializers

from questionnaire.models import DecisionMakers, Tasks, Indicators, Scale


class DecisionMakersRegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = DecisionMakers
        fields = ('id', 'fio', 'login', 'password')


class DecisionMakersSerializers(serializers.ModelSerializer):
    class Meta:
        model = DecisionMakers
        fields = ('id', 'login', 'fio')


class TaskCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'name')


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ('id','grade', 'weight')


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = ('indicator', 'question')


class TaskDetailSerializer(serializers.ModelSerializer):
    # scale = ScaleSerializer(many=True, read_only=True)
    # indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = ('id', 'name', 'description')


class TaskQuestionnaireSerializer(serializers.ModelSerializer):
    scale = ScaleSerializer(many=True, read_only=True)
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = ('description', 'scale', 'indicators')
