# Quickstart: AI-Written Book Generation

**Date**: 2025-11-25
**Feature**: `001-create-ai-book`

This guide provides the steps to set up the development environment, scaffold the Docusaurus project, run the content generation scripts, and serve the website.

## Prerequisites

- **Node.js**: Version `22.20.0` or later.
- **Python**: Version `3.12` or later.
- **`uv`**: The Python package manager. If not installed, you can install it via `pip` or other methods described in the official `uv` documentation.
- **AI Model API Key**: An API key for the generative AI model (e.g., from OpenAI, Google AI). This key must be made available as an environment variable.

## 1. Environment Setup

### a. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### b. Create Project Structure

The project requires a `frontend` and `backend` directory.

```bash
mkdir frontend
mkdir backend
```

### c. Set Up Environment Variables

Create a `.env` file inside the `frontend` directory and add your AI model's API key.

```bash
# frontend/.env
MODEL_API_KEY="your-secret-api-key"
```

### d. Scaffold Docusaurus Project & Install Dependencies

Navigate to the `frontend` directory to scaffold the Docusaurus project and install all necessary dependencies.

```bash
# Navigate to the frontend directory
cd frontend

# Scaffold the Docusaurus project using the classic typescript template
# This command initializes a new Docusaurus site in the current directory.
npx create-docusaurus@latest . classic --typescript

# Install Python dependencies for the content generator using uv
# The requirements.txt is expected to be in frontend/scripts/content-generator/
uv pip install -r scripts/content-generator/requirements.txt
```

## 2. Content Generation

The Python scripts to generate the book chapters are located in `frontend/scripts/content-generator/`.

To run the generation process:

```bash
# Ensure you are in the frontend directory
cd frontend

# Run the main generation script
python scripts/content-generator/main.py
```

The script will:
- Read the chapter list and configuration.
- Generate each chapter as a Markdown file.
- **Place the generated files into the `frontend/docs` folder.**
- Log progress to the console.

## 3. Running the Docusaurus Website

Once the content has been generated, you can start the Docusaurus development server to view the book.

```bash
# Ensure you are in the frontend directory
cd frontend

# Start the Docusaurus development server
npm run start
```

This will start a local development server, and you can view the book in your browser at `http://localhost:3000`.

## 4. Building for Production

To create a production-ready build of the static site for deployment:

```bash
# Ensure you are in the frontend directory
cd frontend

# Build the static site
npm run build
```

The static files will be placed in the `frontend/build` directory, ready to be deployed to a service like GitHub Pages.
