import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# --- Setup ---
# Load environment variables from .env file located at the project root.
load_dotenv()

# Configure logging to display informational messages.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
# Retrieve the Google AI API key from environment variables.
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")

# --- Service Class ---
class AIGoogleService:
    """
    A service class for interacting with the Google AI (Gemini) API.
    This service uses a conversational approach to provide movie recommendations.
    """

    def __init__(self):
        """
        Initializes the AIGoogleService, configures the API key, and sets up
        the conversational model with a system instruction.
        """
        if not GOOGLE_AI_API_KEY:
            logger.error("GOOGLE_AI_API_KEY environment variable not set.")
            raise ValueError("GOOGLE_AI_API_KEY must be set in your environment.")
        
        genai.configure(api_key=GOOGLE_AI_API_KEY)
        
        system_instruction = """You are MirAI, a conversational movie recommendation expert. Your goal is to help users find the perfect movie by having a natural conversation.

RULES:
1.  INFORMATION GATHERING: If the user's request is vague (e.g., "find me a movie", "rekomendasikan film"), your first priority is to ask clarifying questions. Ask about genre, actors, director, mood, or similar movies. Do NOT recommend movies until you have enough specific information (e.g., at least a genre and an actor, or a movie to compare to).
2.  JSON TRIGGER: Once you believe you have gathered enough specific information to make good recommendations, your response MUST BE ONLY a valid JSON object and nothing else. This JSON object should contain a single key "recommendations". The value must be an array of 5 objects, where each object has the keys "title", "year", and "tmdb_id".
3.  NORMAL CONVERSATION: For all other conversation (greetings, follow-up discussion after recommendations, or if the user is just chatting), just respond as a friendly, helpful, and conversational AI movie assistant in the user's language. Do not output JSON in this case.

JSON FORMAT EXAMPLE:
{
  "recommendations": [
    { "title": "Blade Runner 2049", "year": 2017, "tmdb_id": 335984 },
    { "title": "Ex Machina", "year": 2014, "tmdb_id": 264660 }
  ]
}"""

        self.model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            system_instruction=system_instruction
        )

    def get_conversational_response(self, history: list, new_prompt: str) -> str:
        """
        Gets a conversational response from the AI, providing chat history for context.

        Args:
            history (list): A list of previous chat messages.
            new_prompt (str): The new message from the user.

        Returns:
            str: The AI's response, which could be plain text or a JSON string.
        """
        try:
            chat = self.model.start_chat(history=history)
            response = chat.send_message(new_prompt)
            return response.text
        except Exception as e:
            logger.error(f"An unexpected error occurred with Google AI API: {e}")
            return "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."


# --- Example Usage (for direct testing of this script) ---
# if __name__ == '__main__':
#     if not GOOGLE_AI_API_KEY:
#         print("Please set the GOOGLE_AI_API_KEY environment variable in a .env file to run tests.")
#     else:
#         ai_service = AIGoogleService()

#         # --- Test recommendations ---
#         recs = ai_service.get_recommendations("I want a funny sci-fi movie that doesn't take itself too seriously.")
#         if recs:
#             print("--- Recommendations ---")
#             print(json.dumps(recs, indent=2))

#         # --- Test similar movies ---
#         similar = ai_service.suggest_similar_movies("The Matrix")
#         if similar:
#             print("\n--- Similar Movies ---")
#             print(json.dumps(similar, indent=2))
        
#         # --- Test general chat ---
#         chat_resp = ai_service.general_chat("What was the best movie of the 1990s?")
#         if chat_resp:
#             print("\n--- General Chat ---")
#             print(chat_resp['response'])
