# Actionable Tasks: AI-Written Book Generation

**Branch**: `001-ai-book-gen` | **Date**: 2025-11-26
**Spec**: [specs/001-ai-book-gen/spec.md](specs/001-ai-book-gen/spec.md)
**Plan**: [specs/001-ai-book-gen/plan.md](specs/001-ai-book-gen/plan.md)

## Summary

This document outlines the actionable tasks required to implement the AI-Written Book Generation feature, based on the approved specification and implementation plan. Tasks are organized into sequential phases to ensure a logical and dependency-ordered development flow. The primary goal is to leverage existing content generation patterns and components within the `frontend/scripts/content-generator/` directory, extending them to produce Docusaurus-compatible, RAG-optimized Markdown content ready for GitHub Pages deployment.

## Phase 1: Setup

This phase focuses on understanding the existing content generation environment and preparing the workspace for new development.

- [x] T001 Inspect `frontend/scripts/content-generator/` to understand existing structure, language, and LLM integration patterns.
- [x] T002 Review `frontend/scripts/content-generator/requirements.txt` to identify existing Python dependencies.
- [x] T003 Ensure Python 3.9+ environment is available or set up, matching existing `content-generator` setup if applicable.
- [x] T004 Identify the LLM API used in `frontend/scripts/content-generator/` or select a suitable LLM API (e.g., Google Generative AI, OpenAI) based on project standards.
- [x] T005 Configure API keys/credentials for the chosen LLM API securely (e.g., environment variables, `.env` file).

- [x] T005.1 Document findings from T001 (existing structure, language, LLM integration) and update plan.md (Primary Dependencies, LLM API) accordingly.

## Phase 2: Foundational

This phase establishes the core structure and common utilities for the new `book_generator` package, building upon existing patterns.

- [x] T006 Create `frontend/scripts/content-generator/book_generator/` directory.
- [x] T007 Create `frontend/scripts/content-generator/book_generator/__init__.py`.
- [x] T008 Implement `llm_interface.py` to abstract LLM API calls, adapting from existing patterns in `frontend/scripts/content-generator/` if present, or writing afresh. (`frontend/scripts/content-generator/book_generator/llm_interface.py`)
- [x] T009 Implement `file_writer.py` to handle writing Markdown files with Docusaurus Frontmatter, ensuring correct naming conventions (`NN-chapter-title.md`). (`frontend/scripts/content-generator/book_generator/file_writer.py`)
- [x] T010 Implement utility functions for text sanitization, especially for long chapter titles for use in filenames. (`frontend/scripts/content-generator/book_generator/utils.py`)
- [x] T011 Update `frontend/scripts/content-generator/requirements.txt` with any new Python dependencies.

- [x] T011.1 Integrate Flake8 for Python code style enforcement. (frontend/scripts/content-generator/book_generator/.flake8)
- [x] T011.2 Configure Black for automatic Python code formatting. (pyproject.toml or setup.cfg)
- [x] T011.3 Add a pre-commit hook or CI step to enforce linting and formatting. (.pre-commit-config.yaml or .github/workflows/deploy.yml)

## Phase 3: User Story 1 - Generate AI-Written Book Content [US1] (Priority: P1)

**Goal**: Successfully generate all 10 AI-written book chapters in Docusaurus-compatible Markdown format, adhering to all specified content and formatting requirements.
**Independent Test**: Running the main generation script and verifying the creation and structure of the output Markdown files in `frontend/docs/`.

- [x] T012 [US1] Implement `chapter_generator.py` to prompt the LLM for individual chapter content based on title, word count, style, and context of the book. (`frontend/scripts/content-generator/book_generator/chapter_generator.py`)
- [x] T013 [US1] Integrate `llm_interface.py` into `chapter_generator.py` for content generation.
- [x] T014 [US1] Refine `chapter_generator.py` to ensure generated content adheres to heading hierarchy (##, ###, ####) and RAG optimization.
- [x] T015 [US1] Update `main.py` in `frontend/scripts/content-generator/` to orchestrate the book generation process: iterate through chapter titles, call `chapter_generator`, and use `file_writer` to save content to `frontend/docs/`. (`frontend/scripts/content-generator/main.py`)
- [x] T016 [US1] Implement word count validation for each generated chapter to be within 10% of the target.
- [x] T017 [US1] Add error handling for cases where target directory `frontend/docs/` does not exist or is not writable.
- [x] T018 [US1] Add a mechanism to retry LLM calls or provide user feedback on generation failures.

## Phase 4: Polish & Cross-Cutting Concerns

This phase ensures the robustness, testability, and deployability of the new content generation feature.

- [x] T019 Create unit tests for `llm_interface.py`. (`frontend/scripts/content-generator/book_generator/tests/test_llm_interface.py`)
- [x] T020 Create unit tests for `file_writer.py`. (`frontend/scripts/content-generator/book_generator/tests/test_file_writer.py`)
- [x] T021 Create integration tests to verify Docusaurus compatibility of generated Markdown (Frontmatter, heading structure, no manual TOC). (`frontend/scripts/content-generator/tests/test_docusaurus_compatibility.py`)
- [x] T022 Create an end-to-end test that runs the full book generation process and attempts a Docusaurus build using the generated content. (`frontend/scripts/content-generator/tests/test_e2e_book_generation.py`)
- [x] T023 Ensure the generated output is ready for immediate Git commit (e.g., no temporary files, correct permissions).
- [x] T024 Update deployment workflow (`.github/workflows/deploy.yml`) if necessary to include the new content generation step before Docusaurus build for GitHub Pages.

- [x] T024.1 Configure pytest-cov for test coverage reporting. (setup.cfg or pyproject.toml)
- [x] T024.2 Add GitHub Actions step to enforce test coverage threshold. (.github/workflows/deploy.yml)
- [x] T024.3 Implement basic timing for book generation process and log results. (frontend/scripts/content-generator/main.py)

## Dependencies

User Story 1: "Generate AI-Written Book Content" depends on the completion of Phase 1 (Setup) and Phase 2 (Foundational). All tasks within Phase 3 (US1) can be worked on in parallel once their immediate code dependencies are met. Phase 4 (Polish & Cross-Cutting Concerns) depends on the completion of Phase 3.

## Parallel Execution Examples

- **Example 1**: Once Phase 2 is complete, `T012 [US1]` (implement `chapter_generator.py`) and `T015 [US1]` (update `main.py` for orchestration) could potentially be worked on by different developers if the `llm_interface` and `file_writer` are stable.
- **Example 2**: Unit tests (`T019`, `T020`) can be developed in parallel with the implementation of their respective modules (`llm_interface.py`, `file_writer.py`). Integration and E2E tests (`T021`, `T022`) can be started once core generation components are functional.

## Implementation Strategy

The implementation will follow an iterative approach, focusing on delivering a minimum viable product (MVP) for User Story 1 first. This involves setting up the foundational components, then implementing the core chapter generation and orchestration logic. Testing will be integrated throughout the development cycle, with dedicated test tasks for unit, integration, and end-to-end verification. The process aims for continuous integration and readiness for deployment.

**MVP Scope**: Successful generation of all 10 chapters in Docusaurus-compatible Markdown format, saved to `frontend/docs/`, passing basic structure and format validation. This aligns with User Story 1.
