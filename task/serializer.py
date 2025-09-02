from enum import Enum
from rest_framework import serializers

class TaskStatus(Enum):
    PENDING = 'pending'
    DONE = 'done'

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    status= serializers.ChoiceField(choices=[choice.value for choice in TaskStatus], default=TaskStatus.PENDING.value)