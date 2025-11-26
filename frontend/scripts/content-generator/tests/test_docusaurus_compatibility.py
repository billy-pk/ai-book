import pytest
import os
import re
from unittest.mock import MagicMock, patch

# Adjust the path to import necessary modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from book_generator.file_writer import FileWriter

# Mock the logger to prevent actual logging during tests
@pytest.fixture(autouse=True)
def mock_logger():
    with patch('logging.getLogger') as mock_get_logger:
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance
        yield mock_logger_instance

@pytest.fixture
def sample_chapter_data():
    return {
        "position": 1,
        "title": "Introduction to Docusaurus",
        "slug": "introduction-to-docusaurus"
    }

@pytest.fixture
def generated_markdown_content():
    return """## Getting Started
This is an introduction to Docusaurus.

### Installation
Follow these steps:
- Step 1
- Step 2

#### Configuration
Details about configuration.

Some paragraph text.
"""

@pytest.fixture
def output_dir(tmp_path):
    """Provides a temporary output directory for test files."""
    return str(tmp_path)

def test_docusaurus_frontmatter_and_heading_structure(
    sample_chapter_data, generated_markdown_content, output_dir
):
    """
    Tests that a generated Markdown file has correct Docusaurus frontmatter
    and adheres to heading structure rules (no H1, hierarchical).
    """
    file_writer = FileWriter(output_dir)
    file_writer.save_chapter_to_markdown(sample_chapter_data, generated_markdown_content)

    filepath = os.path.join(output_dir, "01-introduction-to-docusaurus.md")
    assert os.path.exists(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Test Frontmatter
    frontmatter_pattern = re.compile(r"^---\nid: introduction-to-docusaurus\ntitle: \"Introduction to Docusaurus\"\n---\n")
    assert frontmatter_pattern.match(content) is not None, "Frontmatter not found or incorrect."

    # Test no H1 (single '#')
    assert re.search(r"^#\s", content, re.MULTILINE) is None, "H1 heading found, which is not Docusaurus compatible for main content."

    # Test for hierarchical headings (starts with H2, then H3, H4)
    # This is a basic check; a full parser would be more robust.
    h2_found = re.search(r"^##\s", content, re.MULTILINE)
    h3_found = re.search(r"^###\s", content, re.MULTILINE)
    h4_found = re.search(r"^####\s", content, re.MULTILINE)

    assert h2_found is not None, "No H2 heading found."
    assert h3_found is not None, "No H3 heading found."
    assert h4_found is not None, "No H4 heading found."

    # Test no manual TOC (Docusaurus generates its own) - difficult to test purely by regex
    # This would typically be a visual check or a more advanced parsing.
    # For now, we assume if the content adheres to headings and is clean, it's compatible.
    
