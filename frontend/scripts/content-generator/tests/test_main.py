import pytest
import os
from unittest.mock import MagicMock, patch
from frontend.scripts.content_generator.main import generate_content, save_chapter_to_markdown, BOOK_STRUCTURE, DOCS_DIR

# Mock the generative AI model for testing generate_content
@pytest.fixture
def mock_genai_model():
    with patch('google.generativeai.GenerativeModel') as MockModel:
        mock_instance = MockModel.return_value
        mock_response = MagicMock()
        mock_response.text = "This is some generated content."
        mock_instance.generate_content.return_value = mock_response
        yield mock_instance

def test_generate_content_success(mock_genai_model):
    """Test successful content generation."""
    prompt = "Test prompt"
    content = generate_content(prompt)
    mock_genai_model.generate_content.assert_called_once_with(prompt)
    assert content == "This is some generated content."

def test_generate_content_error(mock_genai_model):
    """Test content generation with an error."""
    mock_genai_model.generate_content.side_effect = Exception("API error")
    prompt = "Test prompt with error"
    content = generate_content(prompt)
    mock_genai_model.generate_content.assert_called_once_with(prompt)
    assert content == ""

@pytest.fixture
def clean_docs_dir():
    """Ensure the docs directory is clean before and after tests."""
    if os.path.exists(DOCS_DIR):
        for f in os.listdir(DOCS_DIR):
            os.remove(os.path.join(DOCS_DIR, f))
        os.rmdir(DOCS_DIR)
    yield
    if os.path.exists(DOCS_DIR):
        for f in os.listdir(DOCS_DIR):
            os.remove(os.path.join(DOCS_DIR, f))
        os.rmdir(DOCS_DIR)

def test_save_chapter_to_markdown(clean_docs_dir):
    """Test saving generated content to a Markdown file."""
    chapter_data = BOOK_STRUCTURE[0]
    content = "This is the chapter body."
    
    save_chapter_to_markdown(chapter_data, content)

    expected_filename = f"{chapter_data['position']:02d}-{chapter_data['slug']}.md"
    filepath = os.path.join(DOCS_DIR, expected_filename)

    assert os.path.exists(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        file_content = f.read()

    expected_frontmatter = f"""---
id: {chapter_data['slug']}
title: "{chapter_data['title']}"
---
"""
    assert file_content == expected_frontmatter + content
