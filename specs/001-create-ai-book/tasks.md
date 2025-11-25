---

description: "Task list for feature implementation"
---

# Tasks: Create AI-Written Book

**Input**: Design documents from `/specs/001-create-ai-book/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Tasks for testing are included as per the `research.md` testing strategy.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below are adjusted based on `plan.md` structure.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Create root project directories in `/`: `frontend/`, `backend/`
- [x] T002 [P] Create content generator script directories in `frontend/`: `scripts/content-generator/` and `scripts/content-generator/tests/`
- [x] T003 [P] Scaffold Docusaurus project in `frontend/` using `npx create-docusaurus@latest . classic --typescript`
- [x] T004 [P] Create `frontend/scripts/content-generator/requirements.txt` with dependencies: `python-dotenv`, `google-generativeai` (or other AI SDK)
- [x] T005 [P] Install Python dependencies using `uv pip install -r frontend/scripts/content-generator/requirements.txt`
- [x] T006 [P] Create a sample `.env.example` file in `frontend/` with `MODEL_API_KEY=""`
- [x] T007 Configure `pytest` for the Python scripts.
- [x] T008 Configure `Jest` for the Docusaurus frontend.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core content generation script that MUST be complete before user stories can be fully implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T009 Define chapter and book structure in a configuration file or within the main script `frontend/scripts/content-generator/main.py`
- [x] T010 Implement environment variable loading for `MODEL_API_KEY` in `frontend/scripts/content-generator/main.py`
- [x] T011 [P] Implement core AI model communication logic to generate content for a given prompt in `frontend/scripts/content-generator/main.py`
- [x] T012 [P] Implement file-saving logic to write generated content to a Markdown file with Docusaurus frontmatter (`id`, `title`) in `frontend/docs/`
- [x] T013 Implement main loop in `frontend/scripts/content-generator/main.py` to iterate through chapters, generate content, and save files, following the `NN-slug.md` naming convention.
- [x] T014 Implement logging (to console and file) for progress and errors in `frontend/scripts/content-generator/main.py`
- [x] T015 Implement resumption logic to check for existing chapter files and skip generation if they exist in `frontend/scripts/content-generator/main.py`
- [x] T016 Write unit tests for the content generator script's helper functions in `frontend/scripts/content-generator/tests/`

**Checkpoint**: Foundation ready - content generation can now be executed.

---

## Phase 3: User Story 1 - Content Generation (Priority: P1) 🎯 MVP

**Goal**: As a project owner, I want the system to automatically generate 10 chapters of a book on "Impact of AI on School Education" as Markdown files, so that I have the core content of the book ready for review and deployment.

**Independent Test**: The generation process can be run, and the output can be verified by checking for the existence of 10 Markdown files with content that matches the requested chapter titles and approximate word counts.

### Implementation for User Story 1

- [x] T017 [US1] Execute the content generation script by running `python frontend/scripts/content-generator/main.py`
- [x] T018 [US1] Verify that 10 Markdown files are created in `frontend/docs/` with the correct `NN-slugified-chapter-title.md` naming format.
- [x] T019 [US1] Manually review a sample of the generated files to ensure content is relevant, meets word count approximations, and has correct frontmatter.
- [x] T020 [US1] Review logs to ensure no errors were reported during generation.

**Checkpoint**: At this point, User Story 1 should be fully functional. The core book content exists as Markdown files.

---

## Phase 4: User Story 2 - Docusaurus Project Generation (Priority: P2)

**Goal**: As a developer, I want the system to generate a complete Docusaurus project structure, including the generated Markdown files, so that the book can be easily deployed as a static website.

**Independent Test**: The generated Docusaurus project within the `frontend` folder can be built and served. The test passes if the site builds successfully and the content renders correctly.

### Implementation for User Story 2

- [x] T021 [US2] Configure `frontend/docusaurus.config.js` with the book's title, project information, and theme settings.
- [x] T022 [US2] Configure the sidebar in `frontend/docusaurus.config.js` to automatically generate navigation from the files in the `docs/` directory, ensuring correct chapter order.
- [x] T023 [US2] [P] Customize the homepage at `frontend/src/pages/index.js` to serve as a landing page for the book.
- [x] T024 [US2] Start the development server using `npm run start` in the `frontend/` directory and verify the site is accessible and all chapters are present.
- [x] T025 [US2] Navigate through the website to confirm all 10 chapters are listed in the sidebar and render correctly with their on-page table of contents. (Manual verification required by user.)
- [x] T026 [US2] Run `npm run build` in the `frontend/` directory to ensure the production build completes without errors.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work. The book is viewable as a complete website.

---

## Phase 5: User Story 3 - RAG Chatbot Integration Readiness (Priority: P3)

**Goal**: As a future developer, I want the book's content to be structured in a way that allows for easy integration with a RAG chatbot.

**Independent Test**: A sample RAG system can be set up to ingest one of the generated chapter files. The test passes if the RAG system can successfully index the content and answer a simple question based on it.

### Implementation for User Story 3

- [x] T027 [US3] Review the generated Markdown files to confirm a consistent heading structure (`##`, `###`, `####`) is used, which is critical for document chunking.
- [x] T028 [US3] Create a simple validation script (`frontend/scripts/validate_structure.py`) that reads a chapter file and simulates a text-chunking process based on headings to verify logical segmentation.
- [x] T029 [US3] Run the validation script against all generated chapters to programmatically confirm their suitability for RAG ingestion.

**Checkpoint**: All user stories should now be independently functional and validated.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T030 [P] Write comprehensive documentation in a `README.md` at the project root, covering setup, generation, and deployment.
- [x] T031 [P] Code cleanup and refactoring of the generation scripts.
- [x] T032 Run `quickstart.md` validation by having a new team member follow it to set up the project from scratch. (Manual verification required by user.)
- [x] T033 Add a `.gitignore` file to the root directory to exclude `node_modules`, `build` directories, `.env` files, and Python virtual environments.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion. BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
- **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2).
- **User Story 2 (P2)**: Depends on User Story 1. The Docusaurus site needs content to display.
- **User Story 3 (P3)**: Depends on User Story 1. The validation script needs content to analyze.

### Parallel Opportunities

- Most Setup tasks (T002-T008) can run in parallel.
- Within the Foundational phase, AI model logic (T011) and file-saving logic (T012) can be developed in parallel.
- Once the Foundational phase is complete, US2 (Docusaurus config) and US3 (validation script) can begin in parallel while US1 (content generation) is running.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Generate Content)
4. Complete Phase 4: User Story 2 (Configure Docusaurus)
5. **STOP and VALIDATE**: The complete book should be viewable as a static site. This is the core MVP.

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready.
2. Add User Story 1 -> Content is generated.
3. Add User Story 2 -> Website is viewable (MVP!).
4. Add User Story 3 -> Content structure is validated for future work.
5. Complete Polish Phase -> Project is ready for handover/open-sourcing.
