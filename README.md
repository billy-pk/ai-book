# AI Book Project

## Project Title and Description
This project aims to automatically generate a book on "The Impact of AI on School Education" using a generative AI model (Gemini). The generated content is then integrated into a Docusaurus static website for easy review and deployment. The project also includes tools to validate the structure of the generated content for future Retrieval-Augmented Generation (RAG) chatbot integration.

## Features
- Automated generation of book chapters using a configured AI model.
- Integration with Docusaurus for static website generation.
- Consistent Markdown chapter formatting suitable for RAG ingestion.
- Local development server for real-time content review.
- Production build generation for easy deployment.

## Prerequisites
- **Node.js**: Version 20.0 or later (required by Docusaurus).
- **Python**: Version 3.12 or later.
- **`uv`**: The Python package manager. Install via `pip install uv` or other methods in its official documentation.
- **AI Model API Key**: An API key for the generative AI model (e.g., from Google AI Studio). This key must be made available as an environment variable (see Setup Instructions).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-github-username/ai-book.git
cd ai-book
```

### 2. Create Project Structure
The `frontend` and `backend` directories are created. Docusaurus project is scaffolded inside `frontend`.

```bash
# These steps are automated by the development script, but here for reference
mkdir frontend
mkdir backend
# The Docusaurus project is scaffolded into frontend/
npx create-docusaurus@latest frontend classic --typescript
# Python script directories
mkdir -p frontend/scripts/content-generator/tests
```

### 3. Set Up Environment Variables
Create a `.env` file inside the `frontend` directory and add your AI model's API key. Replace `YOUR_GEMINI_API_KEY` with your actual key.

```
# frontend/.env
MODEL_API_KEY="YOUR_GEMINI_API_KEY"
```
Ensure you have a `.env.example` file in `frontend/` with `MODEL_API_KEY=""`.

### 4. Install Dependencies

Navigate to the `frontend` directory to install all necessary dependencies.

```bash
cd frontend

# Install Node.js dependencies for Docusaurus
npm install

# Create Python virtual environment and install Python dependencies for the content generator
cd scripts/content-generator
uv venv
uv pip install -r requirements.txt
cd ../../ # Go back to frontend directory
```

## Content Generation

The Python scripts to generate the book chapters are located in `frontend/scripts/content-generator/`.

To run the generation process (ensure you are in the project root directory):

```bash
# Ensure you are in the project root directory (e.g., ai-book/)
frontend/scripts/content-generator/.venv/bin/python frontend/scripts/content-generator/main.py
```

The script will:
- Read the chapter list and configuration from `main.py`.
- Generate each chapter as a Markdown file using the AI model specified in `main.py` (currently `gemini-2.5-flash-lite`).
- Place the generated files into the `frontend/docs` folder.
- Log progress and errors to `frontend/scripts/content-generator/content_generation.log`.
- Skip generation for chapters that already exist, enabling resumption.

## Running the Docusaurus Website

Once the content has been generated, you can start the Docusaurus development server to view the book.

```bash
# Ensure you are in the frontend directory
cd frontend

# Start the Docusaurus development server
npm run start
```
This will start a local development server, and you can view the book in your browser, typically at `http://localhost:3000/ai-book/`.

## Building for Production

To create a production-ready build of the static site for deployment:

```bash
# Ensure you are in the frontend directory
cd frontend

# Build the static site
npm run build
```
The static files will be placed in the `frontend/build` directory, ready to be deployed to a service like GitHub Pages.

## RAG Integration Readiness

A validation script is available at `frontend/scripts/validate_structure.py` to confirm the consistent heading structure of generated Markdown files, which is critical for document chunking in RAG chatbot integration.

To run the validation script against all generated chapters (ensure you are in the project root directory):
```bash
find frontend/docs -name "[0-9][0-9]-*.md" -print0 | xargs -0 -I {} frontend/scripts/content-generator/.venv/bin/python frontend/scripts/validate_structure.py "{}"
```
This will output the chunked content for each chapter, allowing verification of logical segmentation.
