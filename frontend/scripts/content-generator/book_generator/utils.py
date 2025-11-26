import re
import logging

logger = logging.getLogger(__name__)

def slugify(text: str) -> str:
    """
    Converts a given text into a URL-friendly slug.
    - Converts to lowercase.
    - Replaces non-alphanumeric characters with hyphens.
    - Strips leading/trailing hyphens.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)  # Remove all non-word chars (except spaces and hyphens)
    text = re.sub(r'[\s_-]+', '-', text)  # Replace all whitespace and underscores with a single hyphen
    text = text.strip('-')                # Strip leading/trailing hyphens
    logger.debug(f"Slugified '{text}'")
    return text

def validate_word_count(content: str, target_word_count: int, tolerance_percentage: float = 20.0) -> bool:
    """
    Validates if the word count of the content is within a certain tolerance of the target word count.
    """
    words = content.split()
    actual_word_count = len(words)
    
    lower_bound = target_word_count * (1 - tolerance_percentage / 100)
    upper_bound = target_word_count * (1 + tolerance_percentage / 100)
    
    if lower_bound <= actual_word_count <= upper_bound:
        logger.info(f"Word count {actual_word_count} is within {tolerance_percentage}% of target {target_word_count}.")
        return True
    else:
        logger.warning(f"Word count {actual_word_count} is NOT within {tolerance_percentage}% of target {target_word_count}. "
                       f"Expected range: [{int(lower_bound)}, {int(upper_bound)}]")
        return False
