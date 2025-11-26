import pytest
import os
from unittest.mock import patch, MagicMock

# Adjust the path to import LLMInterface
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from book_generator.llm_interface import LLMInterface

# Fixture to reset the singleton instance before each test
@pytest.fixture(autouse=True)
def reset_llm_interface_singleton():
    LLMInterface._instance = None # Reset the singleton instance
    yield
    LLMInterface._instance = None # Ensure it's reset after the test too

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mocks environment variables for consistent testing."""
    with patch.dict(os.environ, {"MODEL_API_KEY": "fake_api_key"}):
        yield

@pytest.fixture
def mock_genai_configure():
    """Mocks genai.configure."""
    with patch("google.generativeai.configure") as mock_configure:
        yield mock_configure

@pytest.fixture
def mock_generative_model():
    """Mocks genai.GenerativeModel."""
    with patch("google.generativeai.GenerativeModel") as mock_model:
        yield mock_model

def test_llm_interface_singleton_pattern():
    """Tests that LLMInterface adheres to the singleton pattern."""
    instance1 = LLMInterface()
    instance2 = LLMInterface()
    assert instance1 is instance2

def test_llm_interface_initialization(mock_genai_configure, mock_generative_model):
    """Tests successful initialization of LLMInterface."""
    # The _initialize method is called within __new__
    llm_interface = LLMInterface("test-model")
    mock_genai_configure.assert_called_once_with(api_key="fake_api_key")
    mock_generative_model.assert_called_once_with("test-model")
    assert llm_interface.model is mock_generative_model.return_value

def test_llm_interface_initialization_no_api_key():
    """Tests initialization failure when MODEL_API_KEY is missing."""
    with patch.dict(os.environ, {}, clear=True): # Clear environment variables for this test
        # Here, we need to ensure load_dotenv is also mocked or the environment is truly empty
        # A simpler way for testing singletons with env vars is to mock os.getenv directly.
        with patch('os.getenv', return_value=None):
            with pytest.raises(ValueError, match="MODEL_API_KEY not found"):
                LLMInterface()

def test_generate_content_success(mock_generative_model):
    """Tests successful content generation."""
    mock_response = MagicMock()
    mock_response.text = "Generated content"
    mock_generative_model.return_value.generate_content.return_value = mock_response

    llm_interface = LLMInterface() # Initializes and uses the mocked GenerativeModel
    prompt = "Test prompt"
    result = llm_interface.generate_content(prompt)

    mock_generative_model.return_value.generate_content.assert_called_once_with(prompt)
    assert result == "Generated content"

def test_generate_content_failure(mock_generative_model):
    """Tests content generation failure (e.g., API error)."""
    # Configure the mock model to raise an exception
    mock_generative_model.return_value.generate_content.side_effect = Exception("API error")

    llm_interface = LLMInterface()
    prompt = "Test prompt"
    result = llm_interface.generate_content(prompt)

    mock_generative_model.return_value.generate_content.assert_called_once_with(prompt)
    assert result == ""
