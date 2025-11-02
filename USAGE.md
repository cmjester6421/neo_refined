# 📘 NEO Usage Guide

Complete guide to using NEO (Neural Executive Operator) with all available commands and features.

## Table of Contents
- [Getting Started](#getting-started)
- [Interactive Mode](#interactive-mode)
- [Gemini AI Commands](#gemini-ai-commands)
- [System Control Commands](#system-control-commands)
- [Security Commands](#security-commands)
- [Coding Assistant Commands](#coding-assistant-commands)
- [Research Commands](#research-commands)
- [Task Automation](#task-automation)
- [Python API Usage](#python-api-usage)
- [Advanced Features](#advanced-features)

---

## Getting Started

### Launch NEO

**Interactive Mode (Recommended):**
```bash
python -m src.main
# or
neo
```

**Command Mode (Single command):**
```bash
python -m src.main --mode command --command "show system info"
```

**With Custom Config:**
```bash
python -m src.main --config config/neo_config.yaml
```

---

## Interactive Mode

When you start NEO in interactive mode, you'll see:

```
============================================================
🔹 NEO - Neural Executive Operator
Version: 1.0.0
🤖 Gemini AI: Active
============================================================

Type 'help' for available commands, 'exit' to quit.
Special commands: /ai <query>, /code <code>, /solve <problem>

You: 
```

### Basic Interaction

```
You: Hello
NEO: Hello! I'm NEO, your Neural Executive Operator. How can I assist you today?

You: How are you?
NEO: I'm functioning optimally and ready to assist you!

You: exit
NEO: Goodbye! Have a great day!
```

---

## Gemini AI Commands

NEO integrates Google Gemini AI for advanced intelligence. Use these special slash commands:

### 1. `/ai` - Ask Anything

**Direct AI conversation with Gemini**

```
You: /ai What is machine learning?
NEO: Machine learning is a subset of artificial intelligence that enables 
     systems to learn and improve from experience without being explicitly 
     programmed. It focuses on developing algorithms that can access data 
     and use it to learn patterns and make decisions...

You: /ai Explain quantum computing in simple terms
NEO: [Detailed explanation from Gemini AI]

You: /ai Write a haiku about coding
NEO: Lines of code so clean,
     Logic flows like water streams,
     Bugs hide in between.
```

**Use Cases:**
- General questions
- Explanations
- Creative writing
- Brainstorming
- Educational queries

---

### 2. `/code` - Code Analysis

**AI-powered code review and analysis**

**Example 1: Simple Function**
```
You: /code def add(a, b): return a + b
NEO: Code Analysis:
{
  "quality_score": 70,
  "bugs": [],
  "optimizations": [
    "Add type hints for better code documentation",
    "Add docstring to explain function purpose"
  ],
  "security": [],
  "recommendations": [
    "Add input validation",
    "Consider edge cases (None values, wrong types)"
  ]
}
```

**Example 2: Complex Code**
```
You: /code
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

NEO: Code Analysis:
{
  "quality_score": 55,
  "bugs": [
    "Stack overflow for large n values"
  ],
  "optimizations": [
    "Use memoization to avoid redundant calculations",
    "Consider iterative approach for better performance",
    "Time complexity: O(2^n) - very inefficient"
  ],
  "security": [
    "Add input validation to prevent negative values",
    "Add recursion depth limit"
  ],
  "recommendations": [
    "Implement dynamic programming solution",
    "Add type hints: def fibonacci(n: int) -> int",
    "Add docstring with time/space complexity"
  ]
}
```

**Example 3: Web Code**
```javascript
You: /code
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

NEO: Code Analysis:
{
  "quality_score": 60,
  "bugs": [],
  "optimizations": [],
  "security": [
    "CRITICAL: No error handling for failed requests",
    "Add try-catch block",
    "Validate response status before parsing JSON",
    "Add timeout mechanism"
  ],
  "recommendations": [
    "Add error handling",
    "Validate URL before fetching",
    "Add request timeout",
    "Consider retry logic"
  ]
}
```

---

### 3. `/solve` - Problem Solving

**Get AI-powered solutions with step-by-step reasoning**

**Example 1: Algorithm Problem**
```
You: /solve How do I implement a binary search tree?
NEO: Binary Search Tree Implementation:

Step 1: Define the Node Structure
Create a Node class with:
- data (value)
- left child pointer
- right child pointer

Step 2: Implement BST Class
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, data):
        # Insert logic...
    
    def search(self, data):
        # Search logic...
```

Step 3: Key Operations
- Insert: O(log n) average, O(n) worst
- Search: O(log n) average, O(n) worst
- Delete: O(log n) average, O(n) worst

[Detailed explanation continues...]
```

**Example 2: Design Problem**
```
You: /solve How to design a scalable caching system?
NEO: Scalable Caching System Design:

Step 1: Choose Cache Strategy
- LRU (Least Recently Used)
- LFU (Least Frequently Used)
- FIFO (First In First Out)

Step 2: Architecture Components
1. Cache Layer (Redis/Memcached)
2. Application Layer
3. Database Layer

Step 3: Implementation Considerations
- Cache invalidation strategy
- Cache warming
- Distributed caching
- Monitoring and metrics

[Detailed solution with code examples...]
```

**Example 3: Optimization Problem**
```
You: /solve My database queries are slow. How can I optimize them?
NEO: Database Query Optimization Strategy:

Step 1: Identify Bottlenecks
- Use EXPLAIN to analyze query execution
- Check for missing indexes
- Look for N+1 query problems

Step 2: Optimization Techniques
1. Add appropriate indexes
2. Use query caching
3. Optimize JOIN operations
4. Denormalize when appropriate
5. Use connection pooling

[Detailed recommendations continue...]
```

---

### 4. `/summarize` - Text Summarization

**Condense long text into concise summaries**

```
You: /summarize
Artificial intelligence (AI) is revolutionizing various industries by 
automating complex tasks and providing insights from vast amounts of data. 
Machine learning, a subset of AI, enables systems to learn from experience 
without explicit programming. Deep learning uses neural networks with 
multiple layers to process data in increasingly abstract ways. Natural 
language processing allows machines to understand and generate human language. 
Computer vision enables machines to interpret visual information. AI 
applications span healthcare, finance, autonomous vehicles, and more. 
However, ethical considerations around bias, privacy, and job displacement 
remain important challenges to address.

NEO: Summary: AI revolutionizes industries through automation and data 
     insights. Key technologies include machine learning, deep learning, 
     NLP, and computer vision. Applications range from healthcare to 
     autonomous vehicles, but ethical challenges around bias, privacy, 
     and employment persist.
```

---

### 5. `/translate` - Translation

**Translate text to any language**

**Spanish:**
```
You: /translate Spanish Hello, how are you today?
NEO: Translation: Hola, ¿cómo estás hoy?
```

**French:**
```
You: /translate French The weather is beautiful today
NEO: Translation: Le temps est magnifique aujourd'hui
```

**Japanese:**
```
You: /translate Japanese Thank you for your help
NEO: Translation: ご協力ありがとうございます
```

**German:**
```
You: /translate German I would like to learn programming
NEO: Translation: Ich möchte Programmieren lernen
```

**Multiple Sentences:**
```
You: /translate Italian 
Good morning! I hope you're having a wonderful day. 
Let's work together on this project.

NEO: Translation: Buongiorno! Spero che tu stia passando una giornata 
     meravigliosa. Lavoriamo insieme su questo progetto.
```

---

### 6. `/models` - List Available Models

**See what Gemini models are available**

```
You: /models
NEO: Available models:
- models/gemini-2.5-pro
- models/gemini-2.5-flash
- models/gemini-2.0-flash (current)
- models/gemini-2.0-flash-exp
- models/gemini-2.0-flash-thinking-exp
- models/gemini-flash-latest
- models/gemini-pro-latest
[... and 30+ more models]
```

---

### 7. `/help` - Show Help

**Display all available commands**

```
You: /help
NEO: 
Special Commands:
  /ai <query>              - Direct AI query with Gemini
  /code <code>             - Analyze code with AI
  /solve <problem>         - Solve a problem with AI reasoning
  /summarize <text>        - Summarize text
  /translate <lang> <text> - Translate text to target language
  /models                  - List available AI models
  /help                    - Show this help

Regular Commands:
  - Ask questions naturally
  - "show system info" - Get system information
  - "scan ports" - Security scan
  - "analyze code" - Code analysis
  - "research <topic>" - Research a topic
```

---

## System Control Commands

Control and monitor your system with natural language commands.

### System Information

```
You: show system info
NEO: System Information:
     OS: Linux 5.15.0
     CPU Usage: 25.3%
     Memory: 45.2% (3.2GB / 8GB)
     Disk: 67.8% (123GB / 256GB)
     Uptime: 5 days, 3 hours
```

```
You: what is my system status
NEO: [Detailed system status with CPU, memory, disk, network]
```

```
You: check system performance
NEO: [Performance metrics and analysis]
```

### Process Management

```
You: list processes
NEO: Running Processes:
     1. python (PID: 1234) - CPU: 2.3%, Memory: 150MB
     2. chrome (PID: 5678) - CPU: 15.2%, Memory: 890MB
     3. vscode (PID: 9012) - CPU: 5.1%, Memory: 450MB
     [...]
```

```
You: show top processes
NEO: [Top 10 processes by CPU/memory usage]
```

```
You: find process python
NEO: [All Python processes with details]
```

### Resource Monitoring

```
You: check cpu usage
NEO: CPU Usage: 25.3%
     Core 1: 32%
     Core 2: 18%
     Core 3: 29%
     Core 4: 22%
```

```
You: show memory status
NEO: Memory Status:
     Total: 8GB
     Used: 3.2GB (40%)
     Free: 4.8GB (60%)
     Available: 5.1GB
```

```
You: check disk space
NEO: Disk Space:
     / - 123GB / 256GB (48%)
     /home - 89GB / 200GB (44.5%)
```

---

## Security Commands

Advanced security analysis and penetration testing features.

### Password Generation

```
You: generate secure password
NEO: Generated secure password: X9#mK2$pL5@nQ8&vR3

You: generate password 16 characters
NEO: Generated secure password: aB3$xK9@mP7#qR2&sT5wY8
```

### Password Strength Analysis

```
You: check password strength of "password123"
NEO: Password Strength: Weak (score: 25/100)
     Issues:
     - Too common (found in dictionary)
     - No special characters
     - Predictable pattern
     Recommendations:
     - Add special characters
     - Increase length (minimum 12)
     - Avoid common words
```

```
You: analyze password "aB3$xK9@mP7#"
NEO: Password Strength: Strong (score: 85/100)
     ✓ Good length (12 characters)
     ✓ Contains uppercase
     ✓ Contains lowercase
     ✓ Contains numbers
     ✓ Contains special characters
```

### Port Scanning

```
You: scan ports on localhost
NEO: Port Scan Results for localhost:
     Open Ports:
     - 22 (SSH)
     - 80 (HTTP)
     - 443 (HTTPS)
     - 3306 (MySQL)
     Total: 4 open ports found
```

```
You: check open ports
NEO: [Port scan with service detection]
```

### Vulnerability Scanning

```
You: scan for vulnerabilities
NEO: Vulnerability Scan Report:
     Security Score: 75/100
     
     Findings:
     ✓ No SQL injection vulnerabilities detected
     ✓ No XSS vulnerabilities found
     ⚠ Weak password policy detected
     ⚠ Outdated SSL certificate
     
     Recommendations:
     - Update SSL certificate
     - Implement stronger password requirements
```

---

## Coding Assistant Commands

Get help with code development, debugging, and optimization.

### Code Analysis

```
You: analyze this code
NEO: Please provide the code you'd like me to analyze.

You: [paste code]
NEO: Code Analysis:
     Language: Python
     Lines: 45
     Functions: 3
     Classes: 1
     Quality Score: 78/100
     
     Strengths:
     ✓ Good code structure
     ✓ Proper error handling
     ✓ Clear variable names
     
     Improvements:
     - Add type hints
     - Improve documentation
     - Optimize loop in function 'process_data'
```

### Debugging Help

```
You: help debug my code
NEO: I can help with debugging. Please provide:
     1. The code
     2. The error message
     3. What you expected to happen

You: [provide details]
NEO: Debugging Analysis:
     Error: IndexError: list index out of range
     Location: Line 23
     
     Root Cause:
     You're accessing index 5 but the list only has 3 elements
     
     Fix:
     Add bounds checking: if index < len(my_list):
     
     Suggested Code:
     [corrected code example]
```

### Code Optimization

```
You: optimize my code
NEO: [Provide optimization suggestions]

You: how can I make this faster
NEO: Performance Optimization Suggestions:
     1. Use list comprehension instead of loops
     2. Cache repeated calculations
     3. Use built-in functions (they're optimized in C)
     4. Consider using numpy for array operations
     
     Before: O(n²) time complexity
     After:  O(n) time complexity
```

### Documentation Generation

```
You: generate documentation for my code
NEO: Documentation Generated:
     
     """
     Module: data_processor
     
     This module provides functions for processing and analyzing data.
     
     Functions:
         process_data(data: List[Dict]) -> DataFrame
             Process raw data and return cleaned DataFrame
             
         analyze_results(df: DataFrame) -> Dict
             Analyze processed data and return statistics
     """
```

---

## Research Commands

Conduct research on various topics with intelligent analysis.

### Basic Research

```
You: research artificial intelligence
NEO: Research Results for "artificial intelligence":
     
     Summary:
     Artificial intelligence (AI) is the simulation of human intelligence
     in machines programmed to think and learn...
     
     Key Findings:
     - AI market size: $142 billion (2023)
     - Growth rate: 37.3% CAGR
     - Major applications: Healthcare, Finance, Automotive
     
     Sources: 10 sources analyzed
     Confidence: 0.89
```

### Deep Research

```
You: research quantum computing in depth
NEO: Deep Research on "quantum computing":
     
     Overview: [Detailed explanation]
     
     Current State:
     - Technology maturity level
     - Leading companies
     - Recent breakthroughs
     
     Applications:
     1. Cryptography
     2. Drug discovery
     3. Financial modeling
     
     Challenges:
     - Qubit stability
     - Error correction
     - Scaling issues
     
     [More detailed analysis...]
```

### Comparative Research

```
You: compare Python and JavaScript
NEO: Comparative Analysis: Python vs JavaScript
     
     Python:
     ✓ Better for: Data science, ML, scripting
     ✓ Strengths: Clean syntax, rich libraries
     ✗ Weaknesses: Slower execution, GIL
     
     JavaScript:
     ✓ Better for: Web development, real-time apps
     ✓ Strengths: Async capabilities, ubiquitous
     ✗ Weaknesses: Callback hell, type safety
     
     Recommendation: Choose based on use case
```

---

## Task Automation

Automate repetitive tasks and manage workflows.

### Creating Tasks

```
You: create task to backup database
NEO: Task created successfully!
     Task ID: task_001
     Description: Backup database
     Priority: Medium
     Status: Pending
```

### Scheduling Tasks

```
You: schedule task daily at 2am
NEO: Task scheduled:
     Frequency: Daily
     Time: 02:00 AM
     Next run: Tomorrow at 02:00 AM
```

### Task Status

```
You: show task status
NEO: Active Tasks:
     1. Backup database - Running (50% complete)
     2. Clean log files - Pending
     3. Update dependencies - Completed
     
     Completed: 15
     Pending: 2
     Failed: 0
```

---

## Python API Usage

Use NEO programmatically in your Python code.

### Basic Usage

```python
from src.main import NEOAssistant

# Initialize NEO
neo = NEOAssistant()

# Process command
result = neo.process_command("show system info")
print(result['response'])
```

### Using AI Engine

```python
from src.core.ai_engine import NEOAIEngine

# Initialize AI Engine with Gemini
engine = NEOAIEngine(use_gemini=True)

# Generate response
response = engine.generate_response(
    "Explain machine learning",
    temperature=0.7,
    max_tokens=500
)
print(response)

# Analyze code
code = """
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
"""

analysis = engine.analyze_code_with_ai(code, "python")
print(analysis)

# Solve problem
solution = engine.solve_with_ai(
    "How to implement a cache?",
    context="Building a web application"
)
print(solution)
```

### Using Individual Modules

```python
# System Control
from src.modules.system_control import SystemControl
system = SystemControl()
info = system.get_system_info()
print(info)

# Cybersecurity
from src.modules.cybersecurity import CybersecurityModule
security = CybersecurityModule()
password = security.generate_secure_password(16)
print(password)

# Coding Assistant
from src.modules.coding_assistant import CodingAssistant
assistant = CodingAssistant()
analysis = assistant.analyze_code(code, "python")
print(analysis)

# Research
from src.modules.research import ResearchModule
research = ResearchModule()
results = research.research_topic("AI trends", depth="deep")
print(results)
```

### Gemini Integration

```python
from src.core.gemini_integration import GeminiIntegration

# Initialize Gemini
gemini = GeminiIntegration(model_name="gemini-2.0-flash")

# Generate text
response = gemini.generate_text(
    "Write a Python function for binary search",
    temperature=0.5
)
print(response.text)

# Streaming generation
for chunk in gemini.generate_streaming("Tell me a story"):
    print(chunk, end='', flush=True)

# Chat session
chat = gemini.start_chat()
response1 = gemini.chat("What is Python?", chat)
response2 = gemini.chat("What are its benefits?", chat)

# Code analysis
analysis = gemini.analyze_code(code, "python")
print(analysis)

# Translation
translation = gemini.translate_text(
    "Hello, how are you?",
    "Spanish"
)
print(translation)
```

---

## Advanced Features

### Configuration

Edit `config/neo_config.yaml`:

```yaml
ai:
  llm_provider: "gemini"
  gemini_model: "gemini-2.0-flash"
  temperature: 0.7
  max_tokens: 2048

system:
  enable_shutdown: false  # Safety
  enable_restart: false

security:
  enable_port_scanning: true
  password_min_length: 12
```

### Environment Variables

Create/edit `.env`:

```bash
# Gemini API
GEMINI_API_KEY=your_api_key_here

# Environment
NEO_ENV=development
NEO_DEBUG=true

# Logging
LOG_LEVEL=INFO
```

### Custom Commands

Create custom workflows:

```python
from src.main import NEOAssistant

neo = NEOAssistant()

# Custom workflow
def daily_routine():
    # 1. System check
    system_info = neo.process_command("show system info")
    
    # 2. Security scan
    security = neo.process_command("scan for vulnerabilities")
    
    # 3. Backup
    backup = neo.process_command("create backup task")
    
    return {
        'system': system_info,
        'security': security,
        'backup': backup
    }

result = daily_routine()
```

---

## Tips & Best Practices

### 1. Gemini AI Usage

**For factual queries:**
```
You: /ai What is the capital of France?
```

**For code help:**
```
You: /code [paste your code]
```

**For problem-solving:**
```
You: /solve How to optimize database queries?
```

### 2. Temperature Settings

- **0.2-0.3**: Precise, factual (code, documentation)
- **0.7**: Balanced (default, general use)
- **0.9-1.0**: Creative (brainstorming, writing)

### 3. Natural Language

NEO understands natural language:

✓ "show me system info"
✓ "what's my CPU usage"
✓ "can you analyze this code"
✓ "help me debug"
✗ Don't use: systemctl status (use natural language instead)

### 4. Combining Commands

```
You: /ai Based on this code analysis, suggest improvements
[Then paste code analysis results]
NEO: [Detailed suggestions based on analysis]
```

---

## Troubleshooting

### Gemini Not Working

```
You: /ai test
NEO: Gemini AI is not available. Please check your API key.

Fix:
1. Check .env file has GEMINI_API_KEY
2. Run: python scripts/test_gemini.py
3. Verify API key at https://makersuite.google.com/app/apikey
```

### Command Not Recognized

```
NEO: I'm not sure how to help with that. Try /help for available commands.

Fix: Use /help to see all commands, or ask in natural language
```

### Rate Limit Exceeded

```
NEO: Rate limit exceeded. Please try again in a minute.

Fix: Wait 60 seconds, or upgrade to paid tier
```

---

## Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/ai <query>` | Ask AI anything | `/ai What is Docker?` |
| `/code <code>` | Analyze code | `/code def test(): pass` |
| `/solve <problem>` | Solve problems | `/solve How to cache data?` |
| `/summarize <text>` | Summarize text | `/summarize [long text]` |
| `/translate <lang> <text>` | Translate | `/translate Spanish Hello` |
| `/models` | List AI models | `/models` |
| `/help` | Show help | `/help` |
| `show system info` | System info | Natural language |
| `generate password` | Create password | Natural language |
| `research <topic>` | Research topic | `research AI` |
| `exit` | Quit NEO | `exit` |

---

## Getting Help

- **In NEO**: Type `/help` or `help`
- **Documentation**: See `docs/` folder
- **Gemini Guide**: `docs/GEMINI_GUIDE.md`
- **Issues**: GitHub Issues
- **Test**: `python scripts/test_gemini.py`
- **Demo**: `python scripts/demo_gemini.py`

---

**🎉 You're ready to use NEO! Start with simple commands and explore the features.** 🚀
