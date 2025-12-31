from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # The user-facing chat page (e.g., /chat/)
    path('', views.ChatPageView.as_view(), name='page'),
    
    # The API endpoint for programmatic access (e.g., /chat/api/)
    path('api/', views.chat_endpoint, name='api'),
]
