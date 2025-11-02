# 🔹 NEO: Neural Executive Operator

**The Next-Generation AI Assistant for Complete Digital Transformation**

NEO (Neural Executive Operator) is an advanced artificial intelligence assistant designed to revolutionize how you interact with technology. Combining deep learning, neuro learning, recursive learning, and smart thinking capabilities, NEO serves as your ultimate digital agent for handling complex tasks, automations, and intelligent decision-making.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](CHANGELOG.md)

## 🚀 Key Features

- **� Google Gemini AI Integration**: State-of-the-art AI powered by Google's Gemini models
- **�🧠 Advanced Learning Systems**: Deep learning, neuro learning, and recursive learning capabilities
- **🎯 Smart Problem Solving**: Tackles complex problems across mathematics, science, and any subject domain
- **🖥️ Complete PC Control**: Full system automation including shutdown, startup, and complex operations
- **🔒 Cybersecurity Expert**: Advanced penetration testing, security analysis, and threat detection
- **💻 Coding Assistant**: Complete development support with debugging, optimization, and best practices
- **🔬 Research & Development**: Intelligent research capabilities with optimized output generation
- **⚡ Task Automation**: Efficient command execution and decision-making processes
- **💬 Natural Conversations**: Context-aware chat with multi-language support

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Development](#development)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/neo.git
cd neo

# Install NEO
chmod +x scripts/install.sh
./scripts/install.sh

# Activate environment
source venv/bin/activate

# Run NEO
python -m src.main --mode interactive
```

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Option 1: Installation Script (Recommended)

```bash
chmod +x scripts/install.sh
./scripts/install.sh
source venv/bin/activate
```

### Option 2: Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install NEO
pip install -e .
```

### Option 3: Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access NEO
docker exec -it neo-assistant python -m src.main
```

### 🤖 Gemini AI Setup (Optional but Recommended)

To enable advanced AI features powered by Google Gemini:

```bash
# Run the setup script
./scripts/setup_gemini.sh

# Or manually:
# 1. Install the package
pip install google-generativeai

# 2. Get your API key from https://makersuite.google.com/app/apikey

# 3. Add to .env file
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

For detailed Gemini setup and usage, see [Gemini Integration Guide](docs/GEMINI_GUIDE.md).

## 💡 Usage

### Interactive Mode

Start NEO in interactive mode for conversational interaction:

```bash
neo
# or
python -m src.main --mode interactive
```

**Example Session:**
```
You: Hello NEO
NEO: Hello! I'm NEO, your Neural Executive Operator. How can I assist you today?

You: Show me system information
NEO: System: Linux 5.15.0, CPU: 25.3%, Memory: 45.2%

You: /ai Explain quantum computing
NEO: Quantum computing leverages quantum mechanics principles...

You: /code def factorial(n): return n * factorial(n-1) if n > 0 else 1
NEO: Code Analysis: Quality Score: 85/100. Suggestions: Add base case check, use memoization...
```

**Special Gemini Commands:**
- `/ai <query>` - Direct AI conversation
- `/code <code>` - AI-powered code analysis
- `/solve <problem>` - Problem solving with reasoning
- `/summarize <text>` - Summarize long text
- `/translate <lang> <text>` - Translate to any language
- `/help` - Show all commands

### Command Mode

Execute single commands:

```bash
neo --mode command --command "Show system information"
```

### Custom Configuration

```bash
neo --config config/neo_config.yaml
```

## 🎯 Features

### 1. AI Engine

Advanced AI capabilities powered by multiple learning systems:

- **Deep Learning**: Neural network-based processing
- **Neuro Learning**: Pattern recognition and adaptation
- **Recursive Learning**: Iterative problem solving
- **Smart Thinking**: Intelligent decision making

```python
from src.core.ai_engine import NEOAIEngine

engine = NEOAIEngine()
result = engine.process_task({
    'type': 'analysis',
    'description': 'Analyze data',
    'data': your_data
})
```

### 2. System Control

Complete system automation and monitoring:

- System information retrieval
- Process management
- Resource monitoring
- Task scheduling
- Safe command execution

**Commands:**
```
system info
show processes
monitor cpu
monitor memory
```

### 3. Cybersecurity

Professional security analysis tools:

- Port scanning
- Vulnerability assessment
- Password strength analysis
- SQL injection detection
- XSS detection
- Network reconnaissance

**Commands:**
```
generate password
check password [password]
scan ports [target]
security scan [target]
```

### 4. Coding Assistant

Comprehensive development support:

- Code quality analysis
- Bug detection and debugging
- Code optimization
- Documentation generation
- Best practices suggestions

**Commands:**
```
analyze code
debug code
optimize code
format code
```

### 5. Research Module

Intelligent information gathering:

- Multi-source research
- Data analysis (statistical, trend, comparative)
- Web scraping
- Knowledge base management
- Result summarization

**Commands:**
```
research [topic]
find information about [topic]
analyze data
```

### 6. Task Automation

Efficient task management:

- Priority-based task queue
- Multi-threaded execution
- Task scheduling and workflows
- Retry mechanism
- Performance monitoring

```python
from src.modules.task_automation import TaskAutomation, TaskPriority

automation = TaskAutomation(max_workers=5)
task_id = automation.create_task("My Task", my_function, priority=TaskPriority.HIGH)
automation.submit_task(task_id)
```

### 7. NLP Conversation

Natural language understanding:

- Intent detection
- Entity extraction
- Sentiment analysis
- Context management
- Conversation history

## 🏗️ Architecture

```
NEO/
├── src/
│   ├── core/
│   │   └── ai_engine.py          # Core AI engine with learning modules
│   ├── modules/
│   │   ├── system_control.py     # System automation
│   │   ├── cybersecurity.py      # Security tools
│   │   ├── coding_assistant.py   # Code analysis
│   │   ├── research.py           # Research capabilities
│   │   ├── task_automation.py    # Task management
│   │   └── nlp_conversation.py   # NLP and conversation
│   ├── utils/
│   │   ├── logger.py             # Logging system
│   │   └── helpers.py            # Utility functions
│   └── main.py                   # Main application
├── config/
│   ├── settings.py               # Configuration management
│   └── neo_config.yaml           # Default configuration
├── tests/                        # Test suite
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── models/                       # AI models (created at runtime)
└── logs/                         # Log files (created at runtime)
```

## ⚙️ Configuration

### Configuration File

Edit `config/neo_config.yaml`:

```yaml
ai:
  learning_rate: 0.001
  confidence_threshold: 0.8

system:
  enable_shutdown: false  # Safety first!
  max_retries: 3

security:
  enable_port_scanning: true
  password_min_length: 12

task:
  max_workers: 5
```

### Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
# Edit .env with your settings
```

Required variables:
```
NEO_ENV=production
NEO_DEBUG=false
NEO_BASE_DIR=/path/to/neo
```

Optional (for enhanced features):
```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/neo.git
cd neo

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# All tests
./scripts/test.sh

# Specific test file
python -m pytest tests/test_ai_engine.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Maximum line length: 120 characters

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md) - Comprehensive usage guide
- [Development Guide](docs/DEVELOPMENT.md) - Developer documentation
- [API Reference](docs/API.md) - API documentation (coming soon)
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`./scripts/test.sh`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🐛 Bug Reports & Feature Requests

Please use [GitHub Issues](https://github.com/yourusername/neo/issues) to report bugs or request features.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyTorch team for deep learning framework
- FastAPI team for web framework
- All contributors and supporters

## 📞 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/neo/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/neo/discussions)

---

**Built with ❤️ by the NEO Development Team**

*Empowering digital transformation through intelligent automation* 🔹

