import os
import requests
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# --- Setup ---
# Load environment variables from .env file.
# The .env file should be in the root of the Django project.
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_API_URL", "https://api.themoviedb.org/3")

# --- Service Class ---
class TMDBService:
    """
    A service class for interacting with The Movie Database (TMDB) API,
    recreating the logic from the original Express.js service.
    """

    def __init__(self):
        """
        Initializes the TMDBService, ensuring the API key is set.
        """
        if not TMDB_API_KEY:
            logger.error("TMDB_API_KEY environment variable not set.")
            raise ValueError("TMDB_API_KEY must be set in your environment.")
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        A private helper method to make requests to the TMDB API.

        Args:
            endpoint (str): The API endpoint to call (e.g., 'movie/popular').
            params (Optional[Dict[str, Any]]): Additional query parameters.

        Returns:
            Optional[Dict[str, Any]]: The JSON response as a Python dictionary, 
                                      or None if an error occurs.
        """
        url = f"{self.base_url}/{endpoint}"
        
        # Prepare parameters, ensuring the API key is always included
        request_params = {"api_key": self.api_key}
        if params:
            request_params.update(params)

        try:
            response = requests.get(url, params=request_params, timeout=10)
            # Raises an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error for {url}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            # For connection errors, timeouts, etc.
            logger.error(f"Request failed for {url}: {e}")
        except Exception as e:
            # For other unexpected errors, e.g., JSON decoding errors
            logger.error(f"An unexpected error occurred when requesting {url}: {e}")
            
        return None

    def search_movies(self, query: str, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Searches for movies on TMDB based on a query string.
        Corresponds to: GET /search/movie
        """
        params = {"query": query, "page": page, "include_adult": "false"}
        return self._make_request("search/movie", params)

    def get_trending_movies(self, time_window: str = 'week', page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Gets the trending movies on TMDB for a given time window ('day' or 'week').
        Corresponds to: GET /trending/movie/{time_window}
        """
        if time_window not in ['day', 'week']:
            raise ValueError("time_window must be either 'day' or 'week'")
        return self._make_request(f"trending/movie/{time_window}", {"page": page})

    def get_popular_movies(self, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Gets a list of the current popular movies on TMDB.
        Corresponds to: GET /movie/popular
        """
        return self._make_request("movie/popular", {"page": page})

    def get_top_rated_movies(self, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Gets a list of the top-rated movies on TMDB.
        Corresponds to: GET /movie/top_rated
        """
        return self._make_request("movie/top_rated", {"page": page})

    def get_now_playing_movies(self, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Gets a list of movies that are currently playing in theaters.
        Corresponds to: GET /movie/now_playing
        """
        return self._make_request("movie/now_playing", {"page": page})

    def get_upcoming_movies(self, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Gets a list of upcoming movies in theaters.
        Corresponds to: GET /movie/upcoming
        """
        return self._make_request("movie/upcoming", {"page": page})

    def get_movie_details(self, movie_id: int, append_to_response: str = "videos,credits,images") -> Optional[Dict[str, Any]]:
        """
        Gets the primary information for a specific movie.
        'append_to_response' can be a comma-separated list of items to include.
        Corresponds to: GET /movie/{movie_id}
        """
        params = {"append_to_response": append_to_response}
        return self._make_request(f"movie/{movie_id}", params)

    def discover_movies(self, genre: Optional[str] = None, year: Optional[int] = None, rating: Optional[float] = None, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Discovers movies based on filters like genre, year, and rating.
        Corresponds to: GET /discover/movie
        """
        params = {"page": page, "sort_by": "popularity.desc", "include_adult": "false"}
        if genre:
            params["with_genres"] = genre
        if year:
            params["primary_release_year"] = year
        if rating:
            params["vote_average.gte"] = rating
        
        return self._make_request("discover/movie", params)

    def get_genres(self) -> Optional[Dict[str, Any]]:
        """
        Gets the official list of movie genres from TMDB.
        Corresponds to: GET /genre/movie/list
        """
        return self._make_request("genre/movie/list")

# --- Example Usage (for testing) ---
# if __name__ == '__main__':
#     if not TMDB_API_KEY:
#         print("Please set the TMDB_API_KEY environment variable in a .env file to run tests.")
#     else:
#         tmdb_service = TMDBService()
#
#         # --- Test Search ---
#         search_results = tmdb_service.search_movies("Inception")
#         if search_results and search_results.get('results'):
#             print(f"Found {search_results['total_results']} results for 'Inception'.")
#             # print(search_results['results'][0])
#
#         # --- Test Get Details ---
#         # Inception's movie ID is 27205
#         movie_details = tmdb_service.get_movie_details(27205)
#         if movie_details:
#             print(f"Details for movie ID 27205: {movie_details.get('title')}")
#
#         # --- Test Popular ---
#         popular_movies = tmdb_service.get_popular_movies()
#         if popular_movies and popular_movies.get('results'):
#             print(f"Found {len(popular_movies['results'])} popular movies.")
