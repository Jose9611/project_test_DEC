from django.urls import path ,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import login,register_user,TodoListApiView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refresh JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login, name='login'),
    path('register/', register_user, name='register'),
    path('api/', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoListApiView.as_view()),
]