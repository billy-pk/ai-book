---
id: 0024
title: Fix E2E Test Mocked LLM Output
stage: green
date: 2025-11-26
surface: agent
model: gemini-1.5-pro
feature: 001-ai-book-gen
branch: HEAD
user: bilali
command: now  The end-to-end test is failing because the mocked LLM output has only 9 words, which is being rejected by the word count validation logic in main.py.

Action: Modify the mocking setup in the test file tests/test_e2e_book_generation.py to ensure the mock object for the LLM's generate_content method returns a long string (e.g., a sample text of at least 1500 words). The content must be sufficient to pass the word count validation for all chapters in BOOK_STRUCTURE."
labels: ["fix", "tests"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/scripts/content-generator/tests/test_e2e_book_generation.py
tests:
  - tests/test_e2e_book_generation.py
---

## Prompt

```text
now  The end-to-end test is failing because the mocked LLM output has only 9 words, which is being rejected by the word count validation logic in main.py.

Action: Modify the mocking setup in the test file tests/test_e2e_book_generation.py to ensure the mock object for the LLM's generate_content method returns a long string (e.g., a sample text of at least 1500 words). The content must be sufficient to pass the word count validation for all chapters in BOOK_STRUCTURE."
```

## Response snapshot

The `git push origin main` command was successful. The fix for the E2E test failure has been pushed to the remote repository. This should trigger the GitHub Actions workflow.

## Outcome

- ✅ Impact: The `mock_llm_generate_content` fixture in `frontend/scripts/content-generator/tests/test_e2e_book_generation.py` has been updated to return a sufficiently long dummy string (approx. 1500 words). This resolves the word count validation failure in the end-to-end test and should allow the e2e test to pass. The changes have been committed and pushed to the remote repository.
- 🧪 Tests: `frontend/scripts/content-generator/tests/test_e2e_book_generation.py` was modified.
- 📁 Files: `frontend/scripts/content-generator/tests/test_e2e_book_generation.py` was modified.
- 🔁 Next prompts: The user should now monitor their GitHub Actions workflow run to confirm that all tests pass and the deployment to GitHub Pages is successful.
- 🧠 Reflection: Ensuring mock outputs accurately reflect the expected real-world conditions is crucial for reliable test execution, especially when validation logic is involved.

## Evaluation notes (flywheel)

- Failure modes observed: `git commit` output contained spurious shell errors when commit message was improperly formatted, resolved by using multiple `-m` flags.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A