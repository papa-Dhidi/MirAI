import json
import re
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from services.tmdb import TMDBService
from services.ai_google import AIGoogleService
from movies.models import Watchlist

tmdb_service = TMDBService()
ai_service = AIGoogleService()

def home(request):
    """
    Renders the correct homepage based on authentication status.
    - Authenticated users see the main dashboard with personalized recommendations.
    - Unauthenticated users see the landing page.
    """
    if request.user.is_authenticated:
        # Logic for the authenticated user's dashboard
        trending_data = tmdb_service.get_trending_movies()
        ai_recommendations = []
        
        # Get AI recommendations based on the latest watchlist item
        latest_watchlist_item = Watchlist.objects.filter(user=request.user).first()
        if latest_watchlist_item:
            prompt = f"Based on the movie '{latest_watchlist_item.title}', suggest 5 similar movies. You must respond with only a JSON object."
            ai_response_text = ai_service.get_conversational_response(history=[], new_prompt=prompt)
            
            # Clean and parse the response
            cleaned_json_str = ai_response_text
            if '```json' in ai_response_text:
                match = re.search(r"```json\s*(\{.*?\})\s*```", ai_response_text, re.DOTALL)
                if match:
                    cleaned_json_str = match.group(1)

            try:
                parsed_json = json.loads(cleaned_json_str)
                if isinstance(parsed_json, dict) and 'recommendations' in parsed_json:
                    for movie_suggestion in parsed_json['recommendations'][:5]:
                        if 'tmdb_id' in movie_suggestion:
                            details = tmdb_service.get_movie_details(movie_suggestion['tmdb_id'])
                            if details:
                                ai_recommendations.append(details)
            except json.JSONDecodeError:
                # AI didn't return valid JSON, so we'll fall back gracefully
                pass

        # If no AI recommendations could be generated, show popular movies instead.
        if not ai_recommendations:
            popular_data = tmdb_service.get_popular_movies()
            if popular_data and 'results' in popular_data:
                ai_recommendations = popular_data['results'][:5]

        context = {
            'page_title': 'Dashboard',
            'trending_movies': trending_data.get('results', [])[:10] if trending_data else [],
            'ai_recommendations': ai_recommendations,
        }
        return render(request, 'pages/dashboard.html', context)
    else:
        # Show the public landing page
        return render(request, 'pages/landing.html')


class WatchlistPageView(LoginRequiredMixin, ListView):
    """
    Displays the movies in the currently logged-in user's watchlist.
    """
    model = Watchlist
    template_name = 'dashboard/watchlist.html'
    context_object_name = 'watchlist_items'

    def get_queryset(self):
        # Return the watchlist items for the current user
        return Watchlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Watchlist'
        return context


class FavoritesPageView(TemplateView):
    """
    Serves the user's favorites page. (Placeholder)
    """
    template_name = "dashboard/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Favorites'
        context['favorite_items'] = [] # Placeholder
        return context