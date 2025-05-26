from django.urls import path
from .views import RegisterView, PublicRegisterView,CurrentUserView,user_profile

urlpatterns = [
    path('user-profile/', user_profile),
    path('register/', RegisterView.as_view(), name='register'),
    path('public-register/', PublicRegisterView.as_view(), name='public-register'),
    path('user/', CurrentUserView.as_view(), name='user-info'),
]