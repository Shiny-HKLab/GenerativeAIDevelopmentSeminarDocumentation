# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Japanese educational seminar documentation repository for "Generative AI Development Seminar: LLM Application (AI Agent) Development Introduction". The repository contains 8 sections of tutorial materials covering Python API usage, Gemini AI integration, and basic AI agent development concepts.

## Project Structure

- **section01-introduction/**: Basic introduction with simple Python setup
- **section02-jsonplaceholder/**: API fundamentals using requests library and JSONPlaceholder API
  - Contains exercise templates with TODO comments for students
  - Includes solution files in `solution/` directory
  - Has basic pytest tests in `test/` directory
- **section03-basic-gemini-api/**: Google Gemini API integration tutorial
  - Demonstrates google-genai SDK usage
  - Contains Jupyter notebook examples

Each section is structured as an independent Python project with its own pyproject.toml and dependencies.

## Common Development Commands

### Package Management
- Uses `uv` as the primary package manager (uv.lock files present)
- Install dependencies: `uv install` (from section directories)
- Alternative using pip: `pip install -r requirements.txt` (section02 only)

### Testing
- Uses pytest for testing
- Run tests: `pytest` (from section02-jsonplaceholder directory)
- Test files located in `test/` directory

### Running Code
- Execute main scripts: `python main.py` or `python app.py`
- For section02: `python app.py` (contains exercise templates)
- For section03: `python main.py` (basic Gemini API examples)

## Key Dependencies

### Section 2 (JSONPlaceholder API):
- `requests>=2.32.3`: HTTP library for API calls
- `pydantic>=2.11.4`: Data validation and parsing
- `pytest>=8.3.5`: Testing framework
- `ipykernel>=6.29.5`: Jupyter notebook support

### Section 3 (Gemini API):
- `google-genai>=1.11.0`: Google Generative AI SDK
- `python-dotenv>=1.1.0`: Environment variable management
- `requests>=2.32.3`: HTTP library
- `ipykernel>=6.29.5`: Jupyter notebook support

## Architecture Notes

### Educational Structure
- Each section builds upon previous concepts
- Tutorial materials are primarily in Japanese
- Code examples progress from basic HTTP requests to AI SDK integration
- Exercise files contain TODO comments for guided learning

### API Integration Pattern
- Section 2 demonstrates traditional REST API usage with requests library
- Section 3 shows modern SDK-based AI integration
- Both sections include comprehensive error handling examples
- Pydantic models used for data validation and structure

### Exercise Framework
- Template files (app.py) contain skeleton code with TODO markers
- Solution files provided separately in `solution/` directories
- Tests validate both student implementations and provided solutions

## Development Workflow

1. Navigate to specific section directory
2. Install dependencies with `uv install`
3. For exercises: Complete TODO items in template files
4. Run tests to validate implementations: `pytest`
5. Compare with solution files for reference

## Environment Setup

### For Gemini API (Section 3):
- Obtain API key from Google AI Studio
- Set environment variable: `export GOOGLE_API_KEY=your_key_here`
- Or use python-dotenv with .env file

### For Google Colab:
- Use userdata.get("GOOGLE_API_KEY") pattern
- Import keys through Colab secrets interface

## Testing Strategy

- Unit tests focus on API integration functions
- Tests use real external APIs (JSONPlaceholder)
- Assertions validate data structure and content
- Test files import from both exercise templates and solutions