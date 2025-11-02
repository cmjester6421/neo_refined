# Contributing to NEO

Thank you for your interest in contributing to NEO!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Relevant logs

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow PEP 8 style guide
   - Add docstrings to functions/classes
   - Write unit tests
   - Update documentation

4. **Test your changes**
   ```bash
   ./scripts/test.sh
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Create a Pull Request**
   - Describe your changes
   - Reference related issues
   - Include test results

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/neo.git
cd neo

# Install in development mode
./scripts/install.sh
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 120 characters
- Use meaningful variable names
- Write comprehensive docstrings

### Example

```python
def process_data(input_data: List[str], threshold: float = 0.5) -> Dict[str, Any]:
    """
    Process input data and return results.
    
    Args:
        input_data: List of data items to process
        threshold: Minimum confidence threshold (default: 0.5)
    
    Returns:
        Dictionary containing processed results
    
    Raises:
        ValueError: If input_data is empty
    """
    # Implementation
    pass
```

## Testing

- Write unit tests for all new features
- Maintain or improve code coverage
- Test edge cases
- Use meaningful test names

```python
def test_feature_handles_empty_input(self):
    """Test that feature properly handles empty input"""
    result = my_function([])
    self.assertEqual(result, expected_value)
```

## Documentation

- Update README.md for significant changes
- Update USER_GUIDE.md for user-facing features
- Update DEVELOPMENT.md for developer features
- Add inline comments for complex logic

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add entry to CHANGELOG (if exists)
4. Request review from maintainers
5. Address review feedback
6. Merge after approval

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment.

### Our Standards

- Be respectful and professional
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

## Questions?

Feel free to ask questions by creating an issue or reaching out to the maintainers.

Thank you for contributing to NEO! 🔹
