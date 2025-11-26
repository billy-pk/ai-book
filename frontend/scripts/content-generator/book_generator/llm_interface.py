import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Configure logging (assuming it's already set up in main.py, but for standalone use)
logger = logging.getLogger(__name__)

class LLMInterface:
    _instance = None

    def __new__(cls, model_name: str = 'gemini-2.5-flash-lite'):
        if cls._instance is None:
            cls._instance = super(LLMInterface, cls).__new__(cls)
            cls._instance._initialize(model_name)
        return cls._instance

    def _initialize(self, model_name: str):
        load_dotenv()
        MODEL_API_KEY = os.getenv("MODEL_API_KEY")
        if not MODEL_API_KEY:
            logger.error("MODEL_API_KEY not found in environment variables. Please set it in a .env file.")
            raise ValueError("MODEL_API_KEY not found in environment variables. Please set it in a .env file.")

        genai.configure(api_key=MODEL_API_KEY)
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"LLMInterface initialized with model: {model_name}")

    def generate_content(self, prompt: str) -> str:
        """Generates content using the configured AI model."""
        logger.info(f"Generating content for prompt: {prompt[:100]}...")
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return ""
