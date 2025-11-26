import pytest
import os
from unittest.mock import patch, mock_open, MagicMock

# Adjust the path to import FileWriter
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from book_generator.file_writer import FileWriter

@pytest.fixture
def file_writer_instance():
    """Provides a FileWriter instance for testing."""
    test_output_dir = "test_output"
    # Mock os.makedirs to prevent actual directory creation
    with patch("os.makedirs") as mock_makedirs:
        writer = FileWriter(test_output_dir)
        mock_makedirs.assert_called_once_with(test_output_dir, exist_ok=True)
        yield writer

def test_file_writer_initialization(file_writer_instance):
    """Tests successful initialization of FileWriter."""
    assert file_writer_instance.output_dir == "test_output"

def test_save_chapter_to_markdown_success(file_writer_instance):
    """Tests successful saving of a chapter to a Markdown file."""
    chapter_data = {
        "position": 1,
        "title": "Test Chapter Title",
        "slug": "test-chapter-title"
    }
    content = "This is some test content."
    expected_filepath = os.path.join("test_output", "01-test-chapter-title.md")
    expected_frontmatter = """---
id: test-chapter-title
title: "Test Chapter Title"
---
"""
    expected_full_content = expected_frontmatter + content

    with patch("builtins.open", mock_open()) as mock_file_open:
        file_writer_instance.save_chapter_to_markdown(chapter_data, content)
        
        mock_file_open.assert_called_once_with(expected_filepath, 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(expected_full_content)

def test_save_chapter_to_markdown_error(file_writer_instance):
    """Tests error handling during saving a chapter."""
    chapter_data = {
        "position": 2,
        "title": "Error Chapter",
        "slug": "error-chapter"
    }
    content = "Content that should fail."
    expected_filepath = os.path.join("test_output", "02-error-chapter.md")

    with patch("builtins.open", mock_open()) as mock_file_open:
        mock_file_open.side_effect = IOError("Disk full")
        
        with pytest.raises(IOError, match="Disk full"):
            file_writer_instance.save_chapter_to_markdown(chapter_data, content)
        
        mock_file_open.assert_called_once_with(expected_filepath, 'w', encoding='utf-8')