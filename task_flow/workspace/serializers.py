from rest_framework import serializers
from .models import Project, Task, Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "lead", "members"]

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        lead = validated_data.get('lead')

        if lead not in members:
            members.append(lead)

        obj = Workspace.objects.create(**validated_data)
        Workspace.members.through.objects.bulk_create([
            Workspace.members.through(workspace=obj, user=member)
            for member in members
        ])

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
