from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('watchlist/', views.WatchlistPageView.as_view(), name='watchlist'),
    path('favorites/', views.FavoritesPageView.as_view(), name='favorites'),
]
