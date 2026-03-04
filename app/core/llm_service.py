import logging
import hashlib
import json
import os
from typing import Dict, Any, Optional
from app.core.config import settings
from google import genai
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # Configure Gemini (New SDK)
        self.gemini_client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        
        # Configure Groq with a default timeout
        self.groq_client = None
        if settings.GROQ_API_KEY:
            self.groq_client = Groq(
                api_key=settings.GROQ_API_KEY,
                timeout=30.0 # 30s timeout for Groq
            )
            
        # Cache Config
        self.cache_dir = "data/cache"
        self.cache_file = os.path.join(self.cache_dir, "llm_cache.json")
        self._ensure_cache_dir()
        self.cache = self._load_cache()

    def _ensure_cache_dir(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def _load_cache(self) -> Dict[str, str]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

    def _get_cache_key(self, prompt: str, model_type: str) -> str:
        return hashlib.md5(f"{model_type}:{prompt}".encode('utf-8')).hexdigest()

    def generate_content(self, prompt: str, model_type: str = "analyst") -> str:
        """
        Generates content using Gemini (google-genai) with a fallback to Groq.
        """
        # 0. Check Cache First
        cache_key = self._get_cache_key(prompt, model_type)
        if cache_key in self.cache:
            logger.info(f"Using cached response for prompt (key: {cache_key})")
            return self.cache[cache_key]

        # 1. Try Gemini
        try:
            model_name = settings.ANALYST_MODEL if model_type == "analyst" else settings.JUDGE_MODEL
            logger.info(f"Attempting generation with Gemini ({model_name})...")
            
            response = self.gemini_client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={'http_options': {'timeout': 60000}} # 60s timeout in ms
            )
            result = response.text
            
            # Save to cache
            self.cache[cache_key] = result
            self._save_cache()
            return result
        except Exception as e:
            logger.warning(f"Gemini API (google-genai) failed: {str(e)}. Attempting fallback to Groq...")
            
            # 2. Fallback to Groq
            if not self.groq_client:
                return f"LLM Error: Gemini failed and Groq is not configured. Original error: {str(e)}"
            
            try:
                logger.info(f"Attempting fallback with Groq ({settings.GROQ_MODEL})...")
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=settings.GROQ_MODEL,
                )
                result = chat_completion.choices[0].message.content
                
                # Save to cache
                self.cache[cache_key] = result
                self._save_cache()
                return result
            except Exception as groq_e:
                logger.error(f"Groq API also failed: {str(groq_e)}")
                return f"LLM Error: Both Gemini and Groq failed. Gemini error: {str(e)}, Groq error: {str(groq_e)}"

# Global instance
llm_service = LLMService()
