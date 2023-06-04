from .models import Debug, CalledStat
from rest_framework import serializers


class DebugSerializer(serializers.ModelSerializer):

    class Meta:
        model = Debug
        fields = "__all__"


class CallStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalledStat
        fields = "__all__"
