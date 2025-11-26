# Implementation Plan: AI-Written Book Generation

**Branch**: `001-ai-book-gen` | **Date**: 2025-11-26 | **Spec**: [specs/001-ai-book-gen/spec.md](specs/001-ai-book-gen/spec.md)
**Input**: Feature specification from `/specs/001-ai-book-gen/spec.md`

## Summary

The core task is to generate a comprehensive 10-chapter AI-written book as specified in spec.md ("The Transformation of Education: A Guide to Virtual Reality and the Metaverse in K-12"). This book will be generated in Markdown format, specifically tailored for compatibility with Docusaurus, optimized for Retrieval-Augmented Generation (RAG), and structured for seamless deployment via GitHub Pages. The technical approach will prioritize adapting and extending existing content generation scripts within `frontend/scripts/content-generator/` to leverage proven methodologies. New components will only be introduced where existing capabilities cannot fulfill the new requirements, ensuring strict adherence to specified formatting, file naming conventions, Docusaurus Frontmatter, and heading hierarchy requirements.

## Technical Context

**Language/Version**: Python 3.9+ (Leveraging the existing Python environment from `frontend/scripts/content-generator/` and its established LLM SDK compatibility.)  
**Primary Dependencies**:
*   LLM API client (e.g., Google Generative AI SDK, to be confirmed by T001's findings regarding existing content generation tooling).
*   Standard Python libraries for file I/O, string manipulation.
*   No dedicated Markdown generation/parsing library is planned initially; direct string manipulation is expected to be sufficient for Docusaurus-compatible Markdown.
**Storage**: Local filesystem for intermediate and final generated Markdown files (target: `frontend/docs/`).
**Testing**:
*   **Unit Tests**: For individual components like chapter generation logic, file writing with frontmatter, and LLM API interaction.
*   **Integration Tests**: To ensure Docusaurus compatibility (e.g., verifying frontmatter and heading structure), and correct file placement.
*   **End-to-End Tests**: For the complete book generation process, including successful Docusaurus build and readiness for GitHub Pages deployment.
**Target Platform**: Linux server (for execution within GitHub Actions CI/CD environment).
**Project Type**: CLI script (for content generation) interacting with external LLM services, integrated with a Docusaurus frontend.  
**Performance Goals**: Generate all 10 chapters within a reasonable timeframe (e.g., target <30 minutes total generation time, dependent on LLM response times and rate limits).  
**Constraints**: All constraints as defined in the feature specification (spec.md), including Markdown output, Docusaurus compatibility, file naming, Frontmatter requirements, heading hierarchy, RAG optimization, and GitHub Pages deployment readiness.
**Scale/Scope**: Generate 10 distinct book chapters, totaling approximately 15,000 words.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   [x] **I. Code Quality**: Yes, tasks added for linting and formatting enforcement.
*   [x] **II. Testing Standards**: Yes, tasks added for coverage reporting and enforcement.
*   [ ] **III. User Experience Consistency**: N/A for backend content generation script.
*   [x] **IV. Performance Requirements**: Yes, task added for basic performance measurement.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-book-gen/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── scripts/
│   └── content-generator/
│       ├── main.py                     # Orchestration of book generation
│       ├── book_generator/             # New package for generation logic (leveraging existing patterns)
│       │   ├── __init__.py             # Initializes the package
│       │   ├── chapter_generator.py    # Generates content for a single chapter
│       │   ├── file_writer.py          # Handles Markdown file output, naming, frontmatter
│       │   └── llm_interface.py        # Abstraction for interacting with LLM APIs (adapting from existing)
│       └── tests/
│           ├── test_main.py            # Tests for main script orchestration
│           └── test_book_generator.py  # Tests for book_generator components
└── docs/                               # Target directory for generated Markdown files
    ├── 01-preface.md
    ├── 02-fundamentals.md
    ├── 03-tools.md
    ├── 04-curriculum.md
    ├── 05-assessment.md
    ├── 06-design.md
    ├── 07-ethics.md
    ├── 08-future.md
    ├── 09-inclusive.md
    └── 10-policy.md
```

**Structure Decision**: The content generation logic will be encapsulated within a new `book_generator` package under `frontend/scripts/content-generator/` to maintain modularity and integrate with existing script infrastructure. Existing patterns within `content-generator` will be adapted and extended where necessary. The generated Markdown files will be placed directly into `frontend/docs/` as specified.

## Complexity Tracking

(No violations of Constitution Check detected at this planning stage.)