# Contributing to OpenSlots

Thank you for your interest in contributing! This document outlines the process for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry
- AWS CDK CLI
- Docker (for local testing)

### Setting Up Development Environment

1. **Fork the repository**
   - Go to https://github.com/danyalaltaff11555/OpenSlots-lambda
   - Click "Fork" in the top right corner

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/OpenSlots-lambda.git
   cd OpenSlots-lambda
   ```

3. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/danyalaltaff11555/OpenSlots-lambda.git
   ```

4. **Install dependencies**
   ```bash
   poetry install --with infra
   poetry shell
   ```

5. **Set up pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout develop
git merge upstream/develop

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the code standards:
- Use type hints everywhere
- Write docstrings for public functions
- Keep functions small and focused
- Follow PEP 8 (line length: 100)

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_booking_service.py -v
```

### 4. Run Linting and Formatting

```bash
# Check code style
ruff check .

# Auto-format code
black .

# Type checking
mypy src/
```

### 5. Commit Changes

Follow conventional commits:
```
feat: add new feature
fix: fix a bug
refactor: refactor code
docs: update documentation
test: add tests
chore: maintenance
```

### 6. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request via GitHub UI
```

## Code Review Process

1. All PRs require at least one review approval
2. CI/CD must pass all checks
3. Tests must pass
4. Linting and formatting must be clean

## Project Structure

```
OpenSlots-lambda/
├── src/
│   ├── handlers/          # Lambda handlers
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   ├── repositories/      # Data access
│   └── utils/             # Utilities
├── tests/
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── infrastructure/        # AWS CDK
└── docs/                  # Documentation
```

## Adding New Features

1. **Add model** in `src/models/`
2. **Add repository** in `src/repositories/`
3. **Add service** in `src/services/`
4. **Add handler** in `src/handlers/`
5. **Add tests** in `tests/unit/`
6. **Update infrastructure** if needed
7. **Update documentation**

## API Development

When adding new endpoints:
1. Follow REST conventions
2. Add input validation (Pydantic)
3. Use standard response format
4. Add authentication checks
5. Log events appropriately

## Reporting Issues

Use GitHub Issues to report bugs or request features. Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
