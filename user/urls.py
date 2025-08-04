from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', CostumerUserViewSet, basename='user')

urlpatterns = [
    path('create-user/', include(router.urls)),
<<<<<<< HEAD
    path('confirm-email/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
=======
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
>>>>>>> main
]
