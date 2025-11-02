# NEO Development Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Architecture](#architecture)
3. [Module Development](#module-development)
4. [Testing](#testing)
5. [Contributing](#contributing)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/neo.git
cd neo
```

2. Run the installation script:
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Architecture

### Core Components

#### AI Engine (`src/core/ai_engine.py`)
- Deep Learning Module: Neural network processing
- Neuro Learning Module: Pattern recognition
- Recursive Learning Module: Iterative improvement
- Smart Thinking Module: Decision making

#### Modules (`src/modules/`)

1. **System Control**: PC automation and system operations
2. **Cybersecurity**: Security analysis and penetration testing
3. **Coding Assistant**: Code analysis and debugging
4. **Research**: Information gathering and analysis
5. **Task Automation**: Task scheduling and execution
6. **NLP Conversation**: Natural language processing

### Data Flow

```
User Input → NLP Processing → Intent Detection → Module Routing → AI Processing → Response
```

## Module Development

### Creating a New Module

1. Create module file in `src/modules/`:
```python
# src/modules/my_module.py

from src.utils.logger import NEOLogger

class MyModule:
    def __init__(self):
        self.logger = NEOLogger("MyModule")
        self.logger.info("Module initialized")
    
    def process(self, data):
        # Your logic here
        return result
```

2. Register in `src/modules/__init__.py`:
```python
from .my_module import MyModule

__all__ = [..., "MyModule"]
```

3. Integrate in `src/main.py`:
```python
self.my_module = MyModule()
```

### Module Best Practices

- Use NEOLogger for all logging
- Implement error handling
- Add docstrings to all public methods
- Write unit tests
- Follow PEP 8 style guide

## Testing

### Running Tests

```bash
# All tests
./scripts/test.sh

# Specific test file
python -m pytest tests/test_ai_engine.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

```python
import unittest
from src.modules.my_module import MyModule

class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.module = MyModule()
    
    def test_process(self):
        result = self.module.process(data)
        self.assertIsNotNone(result)
```

## Contributing

### Development Workflow

1. Create feature branch:
```bash
git checkout -b feature/my-feature
```

2. Make changes and test:
```bash
# Make changes
./scripts/test.sh
```

3. Commit changes:
```bash
git add .
git commit -m "Add my feature"
```

4. Push and create pull request:
```bash
git push origin feature/my-feature
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions focused
- Maximum line length: 120 characters

### Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues when applicable

## API Reference

### NEOAssistant

Main application class that integrates all modules.

```python
from src.main import NEOAssistant

neo = NEOAssistant()
result = neo.process_command("Your command here")
```

### AI Engine

```python
from src.core.ai_engine import NEOAIEngine

engine = NEOAIEngine()
result = engine.process_task(task_dict)
```

See individual module documentation for detailed API information.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Permission Errors**: Check file permissions and user access

### Debug Mode

Enable debug logging in `.env`:
```
NEO_DEBUG=true
LOG_LEVEL=DEBUG
```

## Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Best Practices](https://docs.python-guide.org/)

---

For more information, visit the [main documentation](README.md).
