from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Project, Task, Workspace
from .serializers import ProjectSerializer, TaskSerializer, WorkspaceSerializer
from .permissions import IsWorkspaceMember


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.select_related('lead').prefetch_related('members')
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('workspace')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceMember]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj.workspace)
        return obj

    def perform_create(self, serializer):
        workspace = get_object_or_404(Workspace, pk=self.kwargs['workspace_pk'])
        serializer.save(workspace=workspace)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceMember]

    def get_queryset(self):
        return (
            Task.objects
            .select_related('assignee', 'project__workspace')
            .filter(
                project__workspace_id=self.kwargs['workspace_pk'],
                project_id=self.kwargs['project_pk']
            )
        )

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj.project.workspace)
        return obj

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['project_pk'],
            workspace_id=self.kwargs['workspace_pk']
        )
        serializer.save(project=project)
