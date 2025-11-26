import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FileWriter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"FileWriter initialized with output directory: {self.output_dir}")

    def save_chapter_to_markdown(self, chapter_data: Dict[str, Any], content: str):
        """
        Saves the generated content to a Markdown file with Docusaurus frontmatter.
        Filename format: NN-slug.md
        """
        filename = f"{chapter_data['position']:02d}-{chapter_data['slug']}.md"
        filepath = os.path.join(self.output_dir, filename)

        frontmatter = f"""---
id: {chapter_data['slug']}
title: "{chapter_data['title']}"
---
"""
        full_content = frontmatter + content

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            logger.info(f"Saved chapter to {filepath}")
        except Exception as e:
            logger.error(f"Error saving chapter to {filepath}: {e}")
            raise