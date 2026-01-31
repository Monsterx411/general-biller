# Contributing to General Biller

First off, thank you for considering contributing to General Biller! It's people like you that make General Biller such a great tool for secure bill payment management.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to maintaining a welcoming and inclusive environment. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Security Vulnerabilities

**DO NOT** create public issues for security vulnerabilities. Instead:

1. Use GitHub Security Advisories to report privately
2. Email security concerns to the repository owner
3. Provide detailed information about the vulnerability
4. Allow reasonable time for a fix before public disclosure

See [SECURITY.md](SECURITY.md) for more details.

## Development Process

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/general-biller.git
   cd general-biller
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install development dependencies
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**
   ```bash
   python -c "from src.models.db import init_db; init_db()"
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed
   - Ensure all tests pass

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

   **Commit Message Guidelines:**
   - Use the present tense ("Add feature" not "Added feature")
   - Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
   - Limit the first line to 72 characters
   - Reference issues and pull requests after the first line

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template with details

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 100 characters
- Use type hints where appropriate

**Example:**
```python
def process_payment(loan_id: str, amount: float) -> dict:
    """
    Process a payment for a loan
    
    Args:
        loan_id: Unique identifier for the loan
        amount: Payment amount in dollars
        
    Returns:
        Dictionary with transaction details
    """
    # Implementation here
    pass
```

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

**Example:**
```python
def test_user_registration_success(client):
    """Test successful user registration"""
    # Arrange
    user_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    
    # Act
    response = client.post('/api/auth/register', json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert 'user' in response.json()
```

### Documentation

- Update README.md if adding user-facing features
- Update API_DOCUMENTATION.md for new API endpoints
- Add docstrings to all new functions and classes
- Update CHANGELOG.md with your changes

## Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest tests/ -v
   ```

2. **Update documentation**
   - Add your changes to CHANGELOG.md
   - Update relevant documentation files
   - Add examples if applicable

3. **Code review**
   - Address all review comments
   - Update your PR as needed
   - Be responsive to feedback

4. **Merge requirements**
   - All tests must pass
   - Code must be reviewed and approved
   - No merge conflicts
   - Documentation updated

## Development Dependencies

Install development dependencies:
```bash
pip install -e ".[dev]"
```

This includes:
- pytest and pytest-cov for testing
- black for code formatting
- flake8 for linting
- mypy for type checking

## Running Tests

### All tests
```bash
pytest tests/ -v
```

### Specific test file
```bash
pytest tests/test_auth.py -v
```

### With coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Linting
```bash
flake8 src/ tests/
```

### Type checking
```bash
mypy src/
```

## Project Structure

Understanding the project structure helps with contributions:

```
general-biller/
├── src/                    # Main source code
│   ├── api/               # Flask API routes
│   ├── models/            # Database models
│   ├── payment/           # Payment processing
│   ├── bank_linking/      # Bank integration
│   └── utils/             # Utilities and helpers
├── tests/                 # Test suite
├── alembic/               # Database migrations
├── frontend/              # Next.js frontend
└── docs/                  # Documentation
```

## License

By contributing to General Biller, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with the tag "question" if you have any questions about contributing.

## Recognition

Contributors will be recognized in:
- GitHub Contributors page
- CHANGELOG.md for significant contributions
- README.md acknowledgments section (for major features)

---

**Thank you for contributing to General Biller!** 🎉

Your contributions help make secure bill payment accessible to everyone.
