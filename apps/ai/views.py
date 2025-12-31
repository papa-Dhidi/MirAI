import json
import re
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from services.ai_google import AIGoogleService
from services.tmdb import TMDBService

# An instance of our services
ai_service = AIGoogleService()
tmdb_service = TMDBService()

class ChatPageView(TemplateView):
    """
    A view to render the user-facing chat page UI.
    """
    template_name = "pages/chat.html"

@csrf_exempt
@require_POST
def chat_endpoint(request):
    """
    A view that acts as a JSON API endpoint for the conversational AI service.
    It passes chat history to the AI and lets the AI decide when to return
    structured data (JSON) for recommendations.
    """
    try:
        data = json.loads(request.body)
        history = data.get('history', [])
        prompt = data.get('prompt')

        if not prompt:
            return JsonResponse({'error': 'Prompt is required.'}, status=400)

        # Get the raw response from the AI (could be text or a JSON string)
        ai_response_text = ai_service.get_conversational_response(history, prompt)

        # --- New: Clean the response to extract JSON from Markdown blocks ---
        cleaned_json_str = ai_response_text
        if '```json' in ai_response_text:
            match = re.search(r"```json\s*(\{.*?\})\s*```", ai_response_text, re.DOTALL)
            if match:
                cleaned_json_str = match.group(1)
        # --------------------------------------------------------------------

        try:
            # Try to parse the (potentially cleaned) response as JSON
            parsed_json = json.loads(cleaned_json_str)
            
            # If it's JSON and contains recommendations, enrich them
            if isinstance(parsed_json, dict) and 'recommendations' in parsed_json:
                enriched_movies = []
                for movie_suggestion in parsed_json['recommendations']:
                    if 'tmdb_id' in movie_suggestion:
                        movie_details = tmdb_service.get_movie_details(movie_suggestion['tmdb_id'])
                        if movie_details:
                            enriched_movies.append(movie_details)
                
                # Return the final, enriched data
                return JsonResponse({'recommendations': enriched_movies})
            
            # If it's valid JSON but not the format we want, return it directly
            return JsonResponse(parsed_json)

        except json.JSONDecodeError:
            # If cleaning fails or it was never JSON, it's a regular text response
            return JsonResponse({'response': ai_response_text})

    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)