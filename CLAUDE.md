# Development Guidelines for Kerykeion

## Core Development Principles

### Project Structure
- Use Poetry for package management
- Configuration in `pyproject.toml`
- Tests in `tests/` directory
- Example scripts in `examples/`

### Package Management
- Use Poetry commands:
  - Install dependencies: `poetry install`
  - Add package: `poetry add package`
  - Development tools: `poetry run tool`

## Code Quality Standards

### Type System
- Type hints recommended but not strictly enforced
- Use `typing` imports where complex types are needed
- Support for Python 3.9+

### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Consistent with project's existing conventions

### Code Style
- Line length: 120 characters (as per Black configuration)
- Use Black for formatting
- Use MyPy for static type checking
- Use pytest for testing

### Functional Principles
- Prefer readability and clarity
- Modular design
- Well-documented public APIs

## Testing Requirements
- Framework: pytest
- Comprehensive test coverage
- Test various scenarios and edge cases
- Regression tests for bug fixes

## Error Handling
- Use specific exceptions where possible
- Provide meaningful error messages
- Use logging for tracking issues

## Development Workflow

### Commit Guidelines
- Descriptive, semantic commit messages
- Clearly explain the purpose of changes
- Reference issues when applicable

### Code Review
- Create detailed PR descriptions
- Focus on code quality and maintainability

## Tools and Validation

### Code Formatting and Checking
1. Black
   - Format: `poetry run black .`
   - Line length: 120 characters

2. MyPy
   - Static type checking: `poetry run mypy`
   - Configuration in `pyproject.toml`

3. Pytest
   - Run tests: `poetry run pytest`
   - Generate coverage reports as needed

## Additional Notes

### Codebase Insights
- Refer to `CODEBASE_MAP.md` for a comprehensive overview of the project structure and components

### Codebase Mapper Instruction
- When running `codebase_mapper`, always update `CODEBASE_MAP.md` to reflect the latest project structure

## Codebase Exploration
- Explore detailed documentation at https://www.kerykeion.net/pydocs/kerykeion.html
- Refer to `CODEBASE_MAP.md` for a high-level project overview

## Licensing
- AGPL-3.0 License
- Contributions welcome
- Open-source collaboration encouraged
