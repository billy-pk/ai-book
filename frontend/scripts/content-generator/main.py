from typing import List, Dict, Any
import os
import logging
import time

from book_generator.llm_interface import LLMInterface
from book_generator.file_writer import FileWriter
from book_generator.chapter_generator import ChapterGenerator
from book_generator.utils import validate_word_count

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

DOCS_DIR = os.path.join(os.path.dirname(__file__), '../../docs') # Relative path to frontend/docs

# Define the book structure (list of chapters)
BOOK_STRUCTURE: List[Dict[str, Any]] = [
    {
        "position": 1,
        "title": "Preface: The New Digital Classroom Frontier",
        "approx_word_count": 1200,
        "slug": "preface-the-new-digital-classroom-frontier"
    },
    {
        "position": 2,
        "title": "Understanding the Metaverse and VR/AR Fundamentals for Learning",
        "approx_word_count": 1500,
        "slug": "understanding-the-metaverse-and-vrar-fundamentals-for-learning"
    },
    {
        "position": 3,
        "title": "Hardware and Software Tools for Immersive Education",
        "approx_word_count": 1500,
        "slug": "hardware-and-software-tools-for-immersive-education"
    },
    {
        "position": 4,
        "title": "Integrating VR/AR into Core Curriculum Subjects",
        "approx_word_count": 1500,
        "slug": "integrating-vrar-into-core-curriculum-subjects"
    },
    {
        "position": 5,
        "title": "Immersive Assessment and Experiential Learning",
        "approx_word_count": 1500,
        "slug": "immersive-assessment-and-experiential-learning"
    },
    {
        "position": 6,
        "title": "Designing and Building Virtual Learning Environments",
        "approx_word_count": 1500,
        "slug": "designing-and-building-virtual-learning-environments"
    },
    {
        "position": 7,
        "title": "Ethical Considerations and Student Safety in Virtual Worlds",
        "approx_word_count": 1500,
        "slug": "ethical-considerations-and-student-safety-in-virtual-worlds"
    },
    {
        "position": 8,
        "title": "The Fully Virtual School: Future Trends and Predictions",
        "approx_word_count": 1500,
        "slug": "the-fully-virtual-school-future-trends-and-predictions"
    },
    {
        "position": 9,
        "title": "VR/AR for Special Education and Diverse Learners",
        "approx_word_count": 1500,
        "slug": "vrar-for-special-education-and-diverse-learners"
    },
    {
        "position": 10,
        "title": "Policy, Governance, and the Future of Educational Technology",
        "approx_word_count": 1200,
        "slug": "policy-governance-and-the-future-of-educational-technology"
    },
]

def main():
    logger.info("Content generator script starting...")
    logger.info("Book structure defined.")

    llm_interface = LLMInterface()
    file_writer = FileWriter(output_dir=DOCS_DIR)
    chapter_generator = ChapterGenerator(llm_interface=llm_interface)

    start_time = time.time() # Start timing

    for chapter_data in BOOK_STRUCTURE:
        chapter_title = chapter_data["title"]
        filename = f"{chapter_data['position']:02d}-{chapter_data['slug']}.md"
        filepath = os.path.join(DOCS_DIR, filename)

        if os.path.exists(filepath):
            logger.info(f"Chapter '{chapter_title}' already exists. Skipping generation.")
            continue
        
        generated_content = chapter_generator.generate_chapter_content(chapter_data)
        if generated_content:
            target_word_count = chapter_data["approx_word_count"]
            if validate_word_count(generated_content, target_word_count):
                file_writer.save_chapter_to_markdown(chapter_data, generated_content)
            else:
                logger.warning(f"Word count validation failed for chapter '{chapter_title}'. Skipping save.")
        else:
            logger.warning(f"Skipping chapter '{chapter_title}' due to content generation failure.")

    end_time = time.time() # End timing
    total_time = end_time - start_time
    logger.info(f"Content generation script finished in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main()

