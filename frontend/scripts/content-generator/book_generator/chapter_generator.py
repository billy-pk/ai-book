import logging
import time
from typing import Dict, Any

from book_generator.llm_interface import LLMInterface

logger = logging.getLogger(__name__)

class ChapterGenerator:
    def __init__(self, llm_interface: LLMInterface, default_word_count: int = 1500, max_retries: int = 3, retry_delay_seconds: int = 5):
        self.llm_interface = llm_interface
        self.default_word_count = default_word_count
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        logger.info("ChapterGenerator initialized.")

    def generate_chapter_content(self, chapter_data: Dict[str, Any], book_context: str = "") -> str:
        """
        Prompts the LLM for individual chapter content based on title, word count, style, and context of the book.
        Includes a retry mechanism for LLM calls.
        """
        chapter_title = chapter_data.get("title", "Untitled Chapter")
        approx_word_count = chapter_data.get("approx_word_count", self.default_word_count)
        slug = chapter_data.get("slug", "untitled-chapter")

        prompt = (
            f"Write a comprehensive chapter titled '{chapter_title}' for a book about 'The Transformation of Education: A Guide to Virtual Reality and the Metaverse in K-12'. "
            f"The chapter should be approximately {approx_word_count} words long. "
            "Ensure the content is well-structured, informative, and engaging. "
            "Use Markdown format with appropriate headings (##, ###) and paragraphs. "
            "Do not include a title at the very beginning of the chapter, it will be added by Docusaurus frontmatter. "
        )
        if book_context:
            prompt += f"Consider the following overall book context: {book_context}"

        generated_content = ""
        for attempt in range(self.max_retries):
            logger.info(f"Attempt {attempt + 1}/{self.max_retries} to generate content for chapter: '{chapter_title}' (Approx {approx_word_count} words)")
            generated_content = self.llm_interface.generate_content(prompt)
            if generated_content:
                logger.info(f"Content generated successfully for chapter: '{chapter_title}'")
                break
            else:
                logger.warning(f"Content generation failed for chapter: '{chapter_title}' on attempt {attempt + 1}. Retrying in {self.retry_delay_seconds} seconds...")
                time.sleep(self.retry_delay_seconds)
        
        if not generated_content:
            logger.error(f"Failed to generate content for chapter: '{chapter_title}' after {self.max_retries} attempts.")

        return generated_content