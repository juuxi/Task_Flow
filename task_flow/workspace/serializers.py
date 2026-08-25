from rest_framework import serializers
from .models import Project, Task, Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "lead", "members"]

    def create(self, validated_data):
        obj = Workspace.objects.create(**validated_data)
        if obj.lead not in obj.members.all():
            obj.members.add(obj.lead)
        return obj


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "workspace"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "deadline",
            "assignee",
            "project",
        ]
