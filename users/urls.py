from django.urls import path
from users.views import RegisterView, LoginView, GetAllUsersView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('getusers/', GetAllUsersView.as_view(), name='getusers'),
]