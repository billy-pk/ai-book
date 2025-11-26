import pytest
import os
from unittest.mock import patch, MagicMock

# Adjust the path to import ChapterGenerator and LLMInterface
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from book_generator.chapter_generator import ChapterGenerator
from book_generator.llm_interface import LLMInterface
from book_generator.utils import slugify, validate_word_count

@pytest.fixture(autouse=True)
def reset_llm_interface_singleton_chapter_generator():
    LLMInterface._instance = None
    yield

@pytest.fixture
def mock_llm_interface():
    """Mocks the LLMInterface instance."""
    with patch('book_generator.llm_interface.LLMInterface') as MockLLMInterface:
        instance = MockLLMInterface.return_value
        yield instance

@pytest.fixture
def chapter_data():
    return {
        "title": "Test Chapter",
        "approx_word_count": 100,
        "slug": "test-chapter"
    }

def test_chapter_generator_initialization(mock_llm_interface):
    """Tests ChapterGenerator initialization."""
    generator = ChapterGenerator(llm_interface=mock_llm_interface, max_retries=2, retry_delay_seconds=1)
    assert generator.max_retries == 2
    assert generator.retry_delay_seconds == 1
    assert generator.llm_interface == mock_llm_interface

def test_generate_chapter_content_success_first_attempt(mock_llm_interface, chapter_data):
    """Tests successful content generation on the first attempt."""
    mock_llm_interface.generate_content.return_value = "Generated Content"
    generator = ChapterGenerator(llm_interface=mock_llm_interface)
    
    content = generator.generate_chapter_content(chapter_data)
    mock_llm_interface.generate_content.assert_called_once()
    assert content == "Generated Content"

def test_generate_chapter_content_success_after_retry(mock_llm_interface, chapter_data):
    """Tests successful content generation after retries."""
    mock_llm_interface.generate_content.side_effect = ["", "", "Generated Content After Retry"]
    generator = ChapterGenerator(llm_interface=mock_llm_interface, max_retries=3, retry_delay_seconds=0.01)
    
    content = generator.generate_chapter_content(chapter_data)
    assert mock_llm_interface.generate_content.call_count == 3
    assert content == "Generated Content After Retry"

def test_generate_chapter_content_failure_after_max_retries(mock_llm_interface, chapter_data):
    """Tests content generation failure after exhausting retries."""
    mock_llm_interface.generate_content.return_value = "" # Always return empty string
    generator = ChapterGenerator(llm_interface=mock_llm_interface, max_retries=2, retry_delay_seconds=0.01)
    
    content = generator.generate_chapter_content(chapter_data)
    assert mock_llm_interface.generate_content.call_count == 2
    assert content == ""

def test_generate_chapter_content_with_book_context(mock_llm_interface, chapter_data):
    """Tests content generation with additional book context."""
    mock_llm_interface.generate_content.return_value = "Generated Content with Context"
    generator = ChapterGenerator(llm_interface=mock_llm_interface)
    book_context = "This book is about testing."
    
    content = generator.generate_chapter_content(chapter_data, book_context=book_context)
    mock_llm_interface.generate_content.assert_called_once()
    args, _ = mock_llm_interface.generate_content.call_args
    assert "Consider the following overall book context: This book is about testing." in args[0]
    assert content == "Generated Content with Context"

def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"

def test_slugify_with_special_chars():
    assert slugify("Chapter 1: AI & Education!!!") == "chapter-1-ai-education"

def test_slugify_with_leading_trailing_spaces():
    assert slugify("  Leading and Trailing  ") == "leading-and-trailing"

def test_slugify_empty_string():
    assert slugify("") == ""

def test_validate_word_count_success_exact():
    content = "word " * 100
    assert validate_word_count(content, 100, 0.0) == True

def test_validate_word_count_success_within_tolerance():
    content = "word " * 110 # 110 words, 10% above 100
    assert validate_word_count(content, 100, 10.0) == True

def test_validate_word_count_failure_above_tolerance():
    content = "word " * 121 # 21% above 100
    assert validate_word_count(content, 100, 20.0) == False

def test_validate_word_count_failure_below_tolerance():
    content = "word " * 79 # 21% below 100
    assert validate_word_count(content, 100, 20.0) == False

def test_validate_word_count_empty_content():
    assert validate_word_count("", 100) == False
