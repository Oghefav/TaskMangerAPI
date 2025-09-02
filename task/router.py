from rest_framework import routers
from task.viewsets import TaskViewSet
router = routers.DefaultRouter()

router.register(r'Task',TaskViewSet, basename='Task')

urlpatterns = [
    *router.urls
]