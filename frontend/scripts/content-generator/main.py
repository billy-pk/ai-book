from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

load_dotenv() # Load environment variables from .env file

# Configure logging
LOG_FILE = os.path.join(os.path.dirname(__file__), 'content_generation.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

MODEL_API_KEY = os.getenv("MODEL_API_KEY")
if not MODEL_API_KEY:
    logger.error("MODEL_API_KEY not found in environment variables. Please set it in a .env file.")
    raise ValueError("MODEL_API_KEY not found in environment variables. Please set it in a .env file.")

genai.configure(api_key=MODEL_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite') # Using gemini-2.5-flash-lite as a default model

def generate_content(prompt: str) -> str:
    """Generates content using the configured AI model."""
    logger.info(f"Generating content for prompt: {prompt[:100]}...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return ""

DOCS_DIR = os.path.join(os.path.dirname(__file__), '../../docs') # Relative path to frontend/docs

def save_chapter_to_markdown(chapter_data: Dict[str, Any], content: str):
    """
    Saves the generated content to a Markdown file with Docusaurus frontmatter.
    Filename format: NN-slug.md
    """
    os.makedirs(DOCS_DIR, exist_ok=True)
    filename = f"{chapter_data['position']:02d}-{chapter_data['slug']}.md"
    filepath = os.path.join(DOCS_DIR, filename)

    frontmatter = f"""---
id: {chapter_data['slug']}
title: "{chapter_data['title']}"
---
"""
    full_content = frontmatter + content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    logger.info(f"Saved chapter to {filepath}")

# Define the book structure (list of chapters)
BOOK_STRUCTURE: List[Dict[str, Any]] = [
    {
        "position": 1,
        "title": "Preface — Why AI Matters in Today’s Classrooms",
        "approx_word_count": 1000,
        "slug": "preface-why-ai-matters-in-todays-classrooms"
    },
    {
        "position": 2,
        "title": "Chapter 1 — The Dawn of AI in Education: A Historical Perspective",
        "approx_word_count": 1500,
        "slug": "the-dawn-of-ai-in-education"
    },
    {
        "position": 3,
        "title": "Chapter 2 — AI-Powered Learning: Personalization and Adaptive Pathways",
        "approx_word_count": 1500,
        "slug": "ai-powered-learning"
    },
    {
        "position": 4,
        "title": "Chapter 3 — The Educator's New Partner: AI Tools for Teaching and Administration",
        "approx_word_count": 1500,
        "slug": "the-educators-new-partner"
    },
    {
        "position": 5,
        "title": "Chapter 4 — Ethical AI in Schools: Navigating Bias, Privacy, and Accountability",
        "approx_word_count": 1500,
        "slug": "ethical-ai-in-schools"
    },
    {
        "position": 6,
        "title": "Chapter 5 — Rethinking Assessment: How AI is Changing Evaluation Methods",
        "approx_word_count": 1500,
        "slug": "rethinking-assessment"
    },
    {
        "position": 7,
        "title": "Chapter 6 — Future-Proofing Education: Skills for an AI-Driven World",
        "approx_word_count": 1500,
        "slug": "future-proofing-education"
    },
    {
        "position": 8,
        "title": "Chapter 7 — Global Perspectives: AI in Education Across Cultures",
        "approx_word_count": 1500,
        "slug": "global-perspectives"
    },
    {
        "position": 9,
        "title": "Chapter 8 — The Human Element: Preserving Creativity and Critical Thinking",
        "approx_word_count": 1500,
        "slug": "the-human-element"
    },
    {
        "position": 10,
        "title": "Conclusion — Charting the Course: The Future of AI in School Education",
        "approx_word_count": 1000,
        "slug": "conclusion-charting-the-course"
    },
]

def main():
    logger.info("Content generator script starting...")
    logger.info("Book structure defined.")

    for chapter_data in BOOK_STRUCTURE:
        chapter_title = chapter_data["title"]
        filename = f"{chapter_data['position']:02d}-{chapter_data['slug']}.md"
        filepath = os.path.join(DOCS_DIR, filename)

        if os.path.exists(filepath):
            logger.info(f"Chapter '{chapter_title}' already exists. Skipping generation.")
            continue
        approx_word_count = chapter_data["approx_word_count"]

        prompt = (
            f"Write a comprehensive chapter titled '{chapter_title}' for a book about 'Impact of AI on School Education'. "
            f"The chapter should be approximately {approx_word_count} words long. "
            "Ensure the content is well-structured, informative, and engaging. "
            "Use Markdown format with appropriate headings (##, ###) and paragraphs. "
            "Do not include a title at the very beginning of the chapter, it will be added by Docusaurus frontmatter."
        )

        generated_content = generate_content(prompt)
        if generated_content:
            save_chapter_to_markdown(chapter_data, generated_content)
        else:
            logger.warning(f"Skipping chapter '{chapter_title}' due to content generation failure.")

    logger.info("Content generation script finished.")

if __name__ == "__main__":
    main()

