import pytest
from unittest.mock import MagicMock, patch
from app.core.llm_service import LLMService

@pytest.fixture
def mock_settings():
    with patch('app.core.llm_service.settings') as m:
        m.GOOGLE_API_KEY = "test_google_key"
        m.GROQ_API_KEY = "test_groq_key"
        m.ANALYST_MODEL = "gemini-1.5-flash"
        m.JUDGE_MODEL = "gemini-1.5-flash"
        m.GROQ_MODEL = "llama3-70b-8192"
        yield m

def test_gemini_success(mock_settings):
    with patch('google.genai.Client') as mock_genai_client:
        # Setup mock for Gemini success
        instance = mock_genai_client.return_value
        instance.models.generate_content.return_value.text = "Gemini Response"
        
        service = LLMService()
        # Ensure we don't use cache for tests
        service.cache = {} 
        response = service.generate_content("Hello Gemini")
        
        assert response == "Gemini Response"

def test_gemini_failure_groq_success(mock_settings):
    with patch('google.genai.Client') as mock_genai_client, \
         patch('app.core.llm_service.Groq') as mock_groq_class:
        
        # Setup Gemini to fail
        instance = mock_genai_client.return_value
        instance.models.generate_content.side_effect = Exception("Gemini Limit Reached")
        
        # Setup Groq to succeed
        mock_groq_instance = mock_groq_class.return_value
        mock_groq_instance.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Groq Fallback Response"))
        ]
        
        service = LLMService()
        service.cache = {}
        response = service.generate_content("Hello Fallback")
        
        assert response == "Groq Fallback Response"
        mock_groq_instance.chat.completions.create.assert_called_once()

def test_both_failure(mock_settings):
    with patch('google.genai.Client') as mock_genai_client, \
         patch('app.core.llm_service.Groq') as mock_groq_class:
        
        # Setup Gemini to fail
        instance = mock_genai_client.return_value
        instance.models.generate_content.side_effect = Exception("Gemini Failure")
        
        # Setup Groq to fail
        mock_groq_instance = mock_groq_class.return_value
        mock_groq_instance.chat.completions.create.side_effect = Exception("Groq Failure")
        
        service = LLMService()
        service.cache = {}
        response = service.generate_content("Hello Total Failure")
        
        assert "LLM Error: Both Gemini and Groq failed" in response
