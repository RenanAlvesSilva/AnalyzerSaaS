from django.urls import path,include 
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('analyzer', AnalyzerViewSet, basename='analyzer')

urlpatterns = [
    path('', include(router.urls)),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]
