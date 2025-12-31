"""
Main URL configuration for the mirAI project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App-specific URLs
    # Include authentication urls (login, logout, signup)
    path('', include('core.urls')),
    
    # The dashboard app will handle the root URLs (e.g., '/', '/watchlist/')
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    
    # URLs for the movies app will be prefixed with /movies/
    path('movies/', include('apps.movies.urls', namespace='movies')),
    
    # URLs for the chat app will be prefixed with /chat/
    path('chat/', include('apps.ai.urls', namespace='chat')),
]

# This is helpful for serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)