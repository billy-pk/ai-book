# Data Model: AI-Written Book

**Date**: 2025-11-25
**Feature**: `001-create-ai-book`

This document outlines the data model for the AI-written book feature, based on the entities identified in the feature specification.

## 1. Book

Represents the entire collection of chapters. This is a singleton entity for the current scope of the project.

### Attributes

| Attribute | Type   | Description                                           | Example                                       |
|-----------|--------|-------------------------------------------------------|-----------------------------------------------|
| Title     | String | The main title of the book.                           | "Impact of AI on School Education"            |
| Chapters  | List   | An ordered list of Chapter entities belonging to the book. | `[Chapter 1, Chapter 2, ...]`                 |

## 2. Chapter

Represents a single chapter of the book. Each chapter will be generated as a separate Markdown file.

### Attributes

| Attribute             | Type    | Description                                                                                             | Example                                                  |
|-----------------------|---------|---------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| **Position / Order**  | Integer | The sequential order of the chapter in the book (1-based). Used for filename prefix and sidebar order.  | `1`                                                      |
| **Title**             | String  | The title of the chapter.                                                                               | "Preface — Why AI Matters in Today’s Classrooms"        |
| **Slug**              | String  | A URL-friendly version of the title used in the filename.                                               | `preface-why-ai-matters-in-todays-classrooms`              |
| **Approx Word Count** | Integer | The target word count for the generated content.                                                        | `1200`                                                   |
| **Generated Content** | String  | The full Markdown content of the chapter, including frontmatter and headings.                           | `--- 
 id: 01-preface... 
 ---

## Introduction...`     |
| **Filename**          | String  | The final filename for the Markdown file, following the `NN-slug.md` format.                              | `01-preface-why-ai-matters-in-todays-classrooms.md`        |

### Relationships

- A **Book** has many **Chapters**.
- A **Chapter** belongs to one **Book**.

### State Transitions

The generation process for each chapter can be viewed as a state machine:

1.  **Pending**: The chapter has not yet been generated.
2.  **Generating**: The AI model is currently generating the content for the chapter.
3.  **Generated**: The content has been successfully generated and saved to a Markdown file.
4.  **Failed**: The generation process failed for this chapter. The system may retry or log the error and skip.
