import sys
import os
import re
from typing import List, Tuple

def chunk_markdown_by_headings(filepath: str) -> List[Tuple[str, str]]:
    """
    Reads a Markdown file and chunks its content based on ##, ###, and #### headings.
    Returns a list of tuples, where each tuple is (heading, content).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find headings and split content.
    # It captures the heading text and the content until the next heading or end of file.
    # This regex is specifically for ##, ###, ####
    # It also handles Docusaurus frontmatter by ignoring content before the first ---
    
    # Remove Docusaurus frontmatter
    frontmatter_match = re.match(r'---\s*\nid:.*\ntitle:.*\n---\s*', content, re.DOTALL)
    if frontmatter_match:
        content = content[frontmatter_match.end():].strip()

    heading_pattern = re.compile(r'(^#{2,4}\s*.*$)', re.MULTILINE)
    
    chunks: List[Tuple[str, str]] = []
    last_end = 0

    for match in heading_pattern.finditer(content):
        heading_text = match.group(1).strip()
        start = match.start()
        
        # Add the content before this heading as part of the previous chunk or as a preamble
        if start > last_end:
            if chunks:
                chunks[-1] = (chunks[-1][0], chunks[-1][1] + content[last_end:start].strip())
            else:
                # This handles any preamble text before the first heading
                preamble_content = content[last_end:start].strip()
                if preamble_content:
                    chunks.append(("Preamble", preamble_content))
        
        chunks.append((heading_text, "")) # Start a new chunk with this heading
        last_end = match.end()

    # Add the remaining content to the last chunk
    if last_end < len(content):
        if chunks:
            chunks[-1] = (chunks[-1][0], chunks[-1][1] + content[last_end:].strip())
        else:
            # Case where there are no headings, just content
            remaining_content = content[last_end:].strip()
            if remaining_content:
                chunks.append(("Full Content", remaining_content))

    return chunks

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_structure.py <markdown_filepath>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        sys.exit(1)
    
    print(f"Processing file: {filepath}\n")
    chunks = chunk_markdown_by_headings(filepath)

    if not chunks:
        print("No headings (##, ###, ####) found, or file is empty after frontmatter removal.")
        return

    for i, (heading, chunk_content) in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(f"Heading: {heading}")
        print(f"Content length: {len(chunk_content)} characters")
        if len(chunk_content) > 200:
            print(f"Content (first 200 chars): {chunk_content[:200]}...")
        else:
            print(f"Content: {chunk_content}")
        print("-" * 20)

if __name__ == "__main__":
    main()
