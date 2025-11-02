# NEO User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Features](#features)
5. [Commands](#commands)
6. [Configuration](#configuration)
7. [Examples](#examples)

## Introduction

NEO (Neural Executive Operator) is an advanced AI assistant that combines deep learning, neuro learning, recursive learning, and smart thinking capabilities to help you with:

- System automation and control
- Cybersecurity and penetration testing
- Code development and debugging
- Research and data analysis
- Task automation
- Intelligent conversations

## Installation

### Using Install Script (Recommended)

```bash
chmod +x scripts/install.sh
./scripts/install.sh
source venv/bin/activate
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install NEO
pip install -e .
```

### Docker Installation

```bash
# Build and run
docker-compose up -d

# Access NEO
docker exec -it neo-assistant python -m src.main
```

## Quick Start

### Interactive Mode

```bash
# Start NEO
python -m src.main --mode interactive

# Or simply
neo
```

### Command Mode

```bash
neo --mode command --command "Show system information"
```

### With Custom Config

```bash
neo --config config/neo_config.yaml
```

## Features

### 1. System Control

Automate system operations and monitor resources.

**Commands:**
- Get system information
- List running processes
- Monitor resources
- Schedule tasks

**Example:**
```
You: Show me system information
NEO: System: Linux 5.15.0, CPU: 25.3%, Memory: 45.2%
```

### 2. Cybersecurity

Advanced security analysis and testing.

**Features:**
- Port scanning
- Vulnerability assessment
- Password analysis
- Security headers check
- SQL injection detection
- XSS detection

**Example:**
```
You: Generate a secure password
NEO: Generated secure password: X9#mK2$pL5@nQ8
```

### 3. Coding Assistant

Comprehensive coding support.

**Features:**
- Code analysis
- Bug detection
- Code optimization
- Documentation generation
- Best practices suggestions

**Example:**
```
You: Analyze this Python code
NEO: Code quality score: 85/100
```

### 4. Research Module

Intelligent research and data gathering.

**Features:**
- Topic research
- Multi-source aggregation
- Data analysis
- Web scraping
- Result summarization

**Example:**
```
You: Research artificial intelligence
NEO: Research completed on 'artificial intelligence' with 0.85 confidence. Found 7 sources.
```

### 5. Task Automation

Efficient task management and scheduling.

**Features:**
- Task creation and management
- Priority-based execution
- Task scheduling
- Workflow automation
- Progress tracking

### 6. Natural Conversation

Context-aware conversations with intent detection.

**Features:**
- Intent recognition
- Entity extraction
- Sentiment analysis
- Context management
- Multi-turn conversations

## Commands

### General Commands

- `help` - Show available commands
- `status` - Show NEO status
- `exit` / `quit` / `bye` - Exit NEO

### System Commands

- `system info` - Display system information
- `show processes` - List running processes
- `monitor cpu` - Monitor CPU usage
- `monitor memory` - Monitor memory usage

### Security Commands

- `generate password` - Generate secure password
- `check password [password]` - Analyze password strength
- `scan ports [target]` - Scan ports on target
- `security scan [target]` - Run vulnerability scan

### Coding Commands

- `analyze code` - Analyze code quality
- `debug code` - Get debugging suggestions
- `optimize code` - Get optimization suggestions
- `format code` - Format code

### Research Commands

- `research [topic]` - Research a topic
- `find information about [topic]` - Find information
- `analyze data` - Analyze data

## Configuration

### Configuration File

Create or edit `config/neo_config.yaml`:

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
NEO_ENV=production
NEO_DEBUG=false
OPENAI_API_KEY=your_key_here
```

## Examples

### Example 1: System Monitoring

```
You: Show me system information
NEO: System: Linux 5.15.0, CPU: 25.3%, Memory: 45.2%

You: What are the top processes?
NEO: Found 10 top processes
```

### Example 2: Password Security

```
You: Generate a strong password
NEO: Generated secure password: X9#mK2$pL5@nQ8

You: Check if "password123" is secure
NEO: Password strength: weak (score: 35/100)
```

### Example 3: Code Analysis

```
You: Analyze my Python function
NEO: Code quality score: 85/100
Issues: 2 minor style issues
Suggestions: Add type hints, improve docstrings
```

### Example 4: Research

```
You: Research machine learning algorithms
NEO: Research completed with 0.85 confidence
Found 7 sources including 3 academic papers
```

## Best Practices

### 1. Start Simple

Begin with basic commands and gradually explore advanced features.

### 2. Use Help

Type `help` anytime to see available commands.

### 3. Review Logs

Check logs in `logs/` directory for detailed information.

### 4. Configure Wisely

Adjust configuration based on your needs and security requirements.

### 5. Keep Updated

Regularly update NEO to get latest features and security patches.

## Troubleshooting

### NEO Won't Start

1. Check Python version: `python --version` (need 3.8+)
2. Verify installation: `pip list | grep neo`
3. Check logs: `cat logs/neo_*.log`

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Permission Issues

```bash
# Fix permissions
chmod +x scripts/*.sh
```

## FAQ

**Q: Is NEO safe to use?**
A: Yes! System-critical operations (like shutdown) are disabled by default.

**Q: Can I add custom modules?**
A: Yes! See the Development Guide for details.

**Q: Does NEO store my data?**
A: NEO stores logs and conversation history locally. Configure retention in settings.

**Q: Can I use NEO programmatically?**
A: Yes! Import and use NEO modules in your Python code.

## Support

For issues, questions, or contributions:
- GitHub Issues: [github.com/yourusername/neo/issues](https://github.com/yourusername/neo/issues)
- Documentation: [docs/](docs/)
- Development Guide: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

---

Happy automating with NEO! 🔹
