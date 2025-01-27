from django.urls import path
from .views import RegisterView, LoginView ,UserDetailAPIView,PostAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailAPIView.as_view(), name='user'),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('post/', PostAPIView.as_view(), name='post'),

]
