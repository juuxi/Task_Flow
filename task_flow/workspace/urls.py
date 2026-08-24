from rest_framework_nested import routers

from . import views

app_name = 'workspace'

router = routers.DefaultRouter()
router.register(r'workspaces', views.WorkspaceViewSet)

workspace_router = routers.NestedDefaultRouter(router, r'workspaces', lookup='workspace')
workspace_router.register(r'projects', views.ProjectViewSet, basename='project')

project_router = routers.NestedDefaultRouter(workspace_router, r'projects', lookup='project')
project_router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = router.urls
urlpatterns += workspace_router.urls
urlpatterns += project_router.urls
