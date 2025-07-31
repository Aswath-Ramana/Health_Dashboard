# Contributing to HIA (Health Insights Agent)

Thank you for considering contributing to HIA! This document provides guidelines and instructions to help you get started.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Development Environment Setup](#development-environment-setup)
  - [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Commit Guidelines](#commit-guidelines)
  - [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We welcome contributions from everyone regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

#### Getting Started 📝

1. Clone the repository:

```bash
git clone https://github.com/Aswath-Ramana/Health_dashboard.git
cd Health_dashboard
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Required environment variables (in `.streamlit/secrets.toml`):

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
GROQ_API_KEY = "your-groq-api-key"
```

4. Set up Supabase database schema:

The application requires the following tables in your Supabase database:

![database schema](https://raw.githubusercontent.com/harshhh28/hia/main/public/db/schema.png)

You can use the SQL script provided at `public/db/script.sql` <a href="https://www.github.com/Aswath-Ramana/Health_dashboard/blob/main/public/db/script.sql">[link]</a> to set up the required database schema.

(PS: You can turn off the email confimation on signup in Supabase settings -> signup -> email)

5. Run the application:

```bash
streamlit run src\main.py
```

## 📁 Project Structure

```
Health_dashboard/
├── requirements.txt
├── README.md
├── src/
│   ├── main.py                 # Application entry point
│   ├── auth/                   # Authentication related modules
│   │   ├── auth_service.py     # Supabase auth integration
│   │   └── session_manager.py  # Session management
│   ├── components/             # UI Components
│   │   ├── analysis_form.py    # Report analysis form
│   │   ├── auth_pages.py       # Login/Signup pages
│   │   ├── footer.py          # Footer component
│   │   └── sidebar.py         # Sidebar navigation
│   ├── config/                # Configuration files
│   │   ├── app_config.py      # App settings
│   │   └── prompts.py         # AI prompts
│   ├── services/              # Service integrations
│   │   └── ai_service.py      # AI service integration
│   ├── agents/                # Agent-based architecture components
│   │   ├── agent_manager.py   # Agent management
│   │   └── model_fallback.py  # Model fallback logic
│   └── utils/                 # Utility functions
│       ├── validators.py      # Input validation
│       └── pdf_extractor.py   # PDF processing
```

## Development Workflow

### Branching Strategy

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Keep your branch updated with the main branch:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

### Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add feature" not "Added feature")
- Reference issue numbers when applicable (e.g., "Fix #123: Update PDF validation")

### Pull Request Process

1. Ensure your code follows the coding standards
2. Update documentation if needed
3. Make sure all tests pass
4. Create a pull request with a clear title and description
5. Link any relevant issues
6. Wait for maintainers to review your PR

## Coding Standards

- Follow Python PEP 8 style guide
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Keep functions focused on a single responsibility
- Organize imports alphabetically within their groups

## Testing

- Test your changes across different environments if possible

## Documentation

- Update the README.md if you add or change features
- Document functions and classes with proper docstrings
- Keep comments up-to-date with code changes

## Issue Reporting

When reporting issues, please include:

1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, etc.)
6. Screenshots if applicable

---

Thank you for contributing! Your efforts help make this project better for everyone. 
