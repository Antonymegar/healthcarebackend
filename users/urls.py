from django.urls import path
from .views import RegisterView, PublicRegisterView,CurrentUserView

urlpatterns = [
    path('admin-register/', RegisterView.as_view(), name='register'),
    path('public-register/', PublicRegisterView.as_view(), name='public-register'),
    path('user/', CurrentUserView.as_view(), name='user-info'),
]