from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from services.tmdb import TMDBService
from movies.models import Watchlist

# Create your views here.
tmdb_service = TMDBService()

def discover_movies_view(request):
    """
    Displays a filterable list of movies from TMDB's /discover endpoint.
    Supports filtering by genre, year, and rating, with pagination.
    """
    # Fetch filter options
    genres_data = tmdb_service.get_genres()
    all_genres = genres_data.get('genres', []) if genres_data else []
    
    # Get filter parameters from request
    selected_genre = request.GET.get('genre')
    selected_year = request.GET.get('year')
    selected_rating = request.GET.get('rating')
    page_number = request.GET.get('page', 1)

    # Fetch discovered movies
    movies_data = tmdb_service.discover_movies(
        genre=selected_genre,
        year=selected_year,
        rating=selected_rating,
        page=page_number
    ) or {}

    context = {
        'page_title': 'Discover Movies',
        'movies': movies_data.get('results', []),
        'genres': all_genres,
        'years': range(2025, 1950, -1), # Year range for dropdown
        'ratings': [i for i in range(1, 10)], # Rating range for dropdown
        'selected_filters': {
            'genre': selected_genre,
            'year': int(selected_year) if selected_year else None,
            'rating': int(selected_rating) if selected_rating else None,
        },
        'pagination': {
            'current_page': movies_data.get('page', 1),
            'total_pages': movies_data.get('total_pages', 1),
            'has_previous': movies_data.get('page', 1) > 1,
            'has_next': movies_data.get('page', 1) < movies_data.get('total_pages', 1),
        }
    }
    
    return render(request, 'pages/movie_list.html', context)


def search_view(request):
    """
    Handles movie searches. Displays a search form and the results.
    """
    query = request.GET.get('query')
    page_number = request.GET.get('page', 1)
    movies_data = None

    if query:
        movies_data = tmdb_service.search_movies(query, page=page_number)

    context = {
        'page_title': f"Search Results for '{query}'" if query else 'Search',
        'query': query,
        'movies': movies_data.get('results', []) if movies_data else [],
        'pagination': {
            'current_page': movies_data.get('page', 1) if movies_data else 1,
            'total_pages': movies_data.get('total_pages', 1) if movies_data else 1,
            'has_previous': movies_data.get('page', 1) > 1 if movies_data else False,
            'has_next': movies_data.get('page', 1) < movies_data.get('total_pages', 1) if movies_data else False,
        } if movies_data else {}
    }
    return render(request, 'pages/search.html', context)


def trending_movies_view(request):
    """
    Displays the top trending movies for the week.
    """
    page_number = request.GET.get('page', 1)
    movies_data = tmdb_service.get_trending_movies(page=page_number)

    context = {
        'page_title': 'Trending Movies',
        'movies': movies_data.get('results', []) if movies_data else [],
        'pagination': {
            'current_page': movies_data.get('page', 1),
            'total_pages': movies_data.get('total_pages', 1),
            'has_previous': movies_data.get('page', 1) > 1,
            'has_next': movies_data.get('page', 1) < movies_data.get('total_pages', 1),
        } if movies_data else {}
    }
    return render(request, 'pages/trending.html', context)


def movie_detail_view(request, movie_id: int):
    """
    Displays the detailed information for a single movie and finds the official trailer.
    """
    movie_details = tmdb_service.get_movie_details(movie_id)
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, movie_id=movie_id).exists()

    # Find the official trailer from the video results
    trailer = None
    if movie_details and 'videos' in movie_details and 'results' in movie_details['videos']:
        for video in movie_details['videos']['results']:
            if video['type'] == 'Trailer' and video['official']:
                trailer = video
                break # Stop after finding the first official trailer
    
    context = {
        'page_title': movie_details.get('title', 'Movie Details') if movie_details else 'Movie not Found',
        'movie': movie_details,
        'is_in_watchlist': is_in_watchlist,
        'trailer': trailer,
    }
    return render(request, 'pages/movie_detail.html', context)


@require_POST
@login_required
def add_to_watchlist(request):
    """
    Adds a movie to the logged-in user's watchlist.
    Expects movie details to be submitted via a POST form.
    """
    movie_id = request.POST.get('movie_id')
    title = request.POST.get('title')
    poster_path = request.POST.get('poster_path')
    release_year_str = request.POST.get('release_year')

    release_year = None
    if release_year_str and release_year_str.isdigit():
        release_year = int(release_year_str)

    if movie_id and title:
        Watchlist.objects.get_or_create(
            user=request.user,
            movie_id=int(movie_id),
            defaults={
                'title': title,
                'poster_path': poster_path,
                'release_year': release_year,
            }
        )
    
    # Redirect back to the previous page, or home if referrer is not available
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:home'))


@require_POST
@login_required
def remove_from_watchlist(request, movie_id: int):
    """
    Removes a movie from the logged-in user's watchlist.
    """
    Watchlist.objects.filter(user=request.user, movie_id=movie_id).delete()
    # Redirect back to the previous page, or home if referrer is not available
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:home'))