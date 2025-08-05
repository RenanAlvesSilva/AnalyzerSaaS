from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', CostumerUserViewSet, basename='user')

urlpatterns = [
    path('create-user/', include(router.urls)),
    path('confirm-email/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', PostResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/<str:uidb64>/<str:token>/', GetResetPasswordView.as_view(), name='reset_password_confirm'),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]
