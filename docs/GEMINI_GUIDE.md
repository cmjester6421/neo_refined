# 🤖 Gemini AI Integration Guide for NEO

## Overview

NEO now integrates **Google Gemini AI** for enhanced intelligence capabilities. Gemini provides state-of-the-art natural language understanding, code analysis, reasoning, and problem-solving.

## Features

### 🧠 Advanced AI Capabilities

- **Natural Language Understanding**: Ask complex questions and get intelligent responses
- **Code Analysis**: Deep code review with security and performance insights
- **Problem Solving**: Step-by-step reasoning for complex problems
- **Text Summarization**: Summarize long documents efficiently
- **Translation**: Multi-language translation support
- **Conversational AI**: Context-aware conversations

## Setup

### 1. Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Gemini Package

**Quick Setup (Recommended):**
```bash
./scripts/setup_gemini.sh
```

**Manual Setup:**
```bash
# Install the package
pip install google-generativeai

# Add your API key to .env
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

### 3. Verify Installation

```bash
python -c "import google.generativeai as genai; print('✅ Gemini is ready!')"
```

## Usage

### Interactive Mode Commands

NEO provides special slash commands for direct Gemini interaction:

#### `/ai` - Direct AI Query
Ask Gemini anything directly:
```
You: /ai What is quantum computing?
NEO: [Detailed explanation from Gemini]

You: /ai Explain machine learning to a 10-year-old
NEO: [Child-friendly explanation]
```

#### `/code` - Code Analysis
Analyze code with AI-powered insights:
```
You: /code def bubble_sort(arr): ...
NEO: Code Analysis:
{
  "quality_score": 75,
  "bugs": ["No input validation", "Inefficient for large arrays"],
  "optimizations": ["Use quicksort for better performance"],
  "security": ["Add input type checking"],
  "recommendations": ["Add docstrings", "Use type hints"]
}
```

#### `/solve` - Problem Solving
Get step-by-step solutions:
```
You: /solve How do I implement a binary search tree?
NEO: [Detailed solution with reasoning]
```

#### `/summarize` - Text Summarization
Summarize long text:
```
You: /summarize [long article text]
NEO: Summary: [Concise summary in ~200 words]
```

#### `/translate` - Translation
Translate text to any language:
```
You: /translate Spanish Hello, how are you?
NEO: Translation: Hola, ¿cómo estás?

You: /translate French The weather is nice today
NEO: Translation: Le temps est agréable aujourd'hui
```

#### `/models` - List Available Models
See what Gemini models you can use:
```
You: /models
NEO: Available models:
- models/gemini-pro
- models/gemini-pro-vision
```

#### `/help` - Show Help
Display all available commands:
```
You: /help
NEO: [Shows complete command list]
```

### Programmatic Usage

Use Gemini in your Python code:

```python
from src.core.ai_engine import NEOAIEngine

# Initialize with Gemini
engine = NEOAIEngine(use_gemini=True, gemini_model="gemini-pro")

# Generate response
response = engine.generate_response(
    "Explain the theory of relativity",
    temperature=0.7
)
print(response)

# Analyze code
analysis = engine.analyze_code_with_ai("""
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
""", language="python")
print(analysis)

# Solve problem
solution = engine.solve_with_ai(
    "How to optimize database queries?",
    context="PostgreSQL database with millions of records"
)
print(solution)

# Chat
response = engine.chat_with_gemini("What's the best sorting algorithm?")
print(response)
```

### Direct Gemini Integration

For advanced use cases:

```python
from src.core.gemini_integration import GeminiIntegration

# Create client
gemini = GeminiIntegration(model_name="gemini-pro")

# Generate text
response = gemini.generate_text(
    "Write a Python function to calculate fibonacci numbers",
    temperature=0.5,
    max_tokens=1024
)
print(response.text)

# Streaming generation
for chunk in gemini.generate_streaming("Tell me a story"):
    print(chunk, end='', flush=True)

# Start chat session
chat = gemini.start_chat()
response1 = gemini.chat("What is Python?", chat)
response2 = gemini.chat("What are its main features?", chat)

# Count tokens
token_count = gemini.count_tokens("This is a sample text")
print(f"Tokens: {token_count}")
```

## Configuration

### Model Selection

Edit `config/neo_config.yaml`:

```yaml
ai:
  llm_provider: "gemini"  # Options: gemini, openai, anthropic, local
  gemini_model: "gemini-pro"
  temperature: 0.7
  max_tokens: 2048
```

### Available Models

- **gemini-pro**: Best for text-based tasks
- **gemini-pro-vision**: For image + text tasks (future support)

### Temperature Settings

- `0.0-0.3`: Precise, deterministic (good for code, facts)
- `0.4-0.7`: Balanced (default, good for general use)
- `0.8-1.0`: Creative, diverse (good for brainstorming)

## Examples

### Example 1: Code Review

```
You: /code
def login(username, password):
    if username == "admin" and password == "password":
        return True
    return False

NEO: Code Analysis:
{
  "quality_score": 45,
  "bugs": [],
  "optimizations": [
    "Use constant-time comparison to prevent timing attacks"
  ],
  "security": [
    "CRITICAL: Hardcoded credentials",
    "CRITICAL: Plaintext password comparison",
    "Use password hashing (bcrypt/argon2)",
    "Implement rate limiting",
    "Add account lockout after failed attempts"
  ],
  "recommendations": [
    "Use environment variables for credentials",
    "Implement proper authentication system",
    "Add logging for security events"
  ]
}
```

### Example 2: Research Assistant

```
You: /ai What are the latest advances in quantum computing?

NEO: Recent advances in quantum computing include:

1. **Quantum Advantage**: Google's Sycamore achieved quantum supremacy...
2. **Error Correction**: IBM developed new error correction codes...
3. **Quantum Networks**: Successful quantum teleportation over 44km...
4. **Applications**: Drug discovery, cryptography, optimization...

[Detailed explanation continues...]
```

### Example 3: Problem Solving

```
You: /solve How to design a scalable microservices architecture?

NEO: Designing a Scalable Microservices Architecture:

Step 1: Domain-Driven Design
- Identify bounded contexts
- Define service boundaries
- Establish communication patterns

Step 2: Service Design
- Single Responsibility Principle
- Independent deployment
- Database per service

[Detailed solution with reasoning...]
```

## API Limits & Pricing

### Free Tier
- 60 requests per minute
- 1,500 requests per day
- 1 million tokens per month

### Rate Limiting
NEO automatically handles rate limits and retries failed requests.

### Cost Optimization
```python
# Use lower temperature for deterministic results (fewer tokens)
engine.generate_response(prompt, temperature=0.2)

# Limit max tokens
engine.generate_response(prompt, max_tokens=500)

# Cache frequently asked questions
# NEO automatically caches responses
```

## Troubleshooting

### "Gemini AI not available"

**Solution:**
```bash
# Check if package is installed
pip list | grep google-generativeai

# Install if missing
pip install google-generativeai
```

### "API key not found"

**Solution:**
```bash
# Check .env file
cat .env | grep GEMINI

# Add key if missing
echo "GEMINI_API_KEY=your_key_here" >> .env
```

### "Rate limit exceeded"

**Solution:**
- Wait a minute and try again
- Reduce request frequency
- Consider upgrading to paid tier

### Import Error

**Solution:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall package
pip install --upgrade google-generativeai
```

## Best Practices

### 1. Prompt Engineering

**Good:**
```
You: /ai Explain recursion with a Python example and time complexity analysis
```

**Better:**
```
You: /solve Problem: Implement a recursive function to calculate factorial.
Context: Need to understand both recursive and iterative approaches.
Requirements: Include time/space complexity and optimization tips.
```

### 2. Context Management

```python
# Provide context for better responses
engine.chat_with_gemini(
    "How do I optimize this?",
    context=[
        {"role": "user", "content": "I'm working on a web scraper"},
        {"role": "assistant", "content": "I can help optimize your scraper"}
    ]
)
```

### 3. Error Handling

```python
try:
    response = engine.generate_response(query)
except Exception as e:
    print(f"Gemini error: {e}")
    # Fallback to local AI
    response = engine.nlp.generate_response(session, query)
```

## Advanced Features

### Safety Settings

```python
import google.generativeai as genai

# Configure safety settings
safety_settings = [
    {
        "category": genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    }
]

# Use in generation
gemini.generate_text(prompt, safety_settings=safety_settings)
```

### Token Counting

```python
# Check tokens before sending
token_count = engine.gemini.count_tokens(long_prompt)
if token_count > 30000:
    print("Warning: Prompt too long")
```

### Model Switching

```python
# Switch to different model
engine.switch_gemini_model("gemini-pro-vision")

# Check available models
models = engine.get_gemini_models()
```

## Resources

- 📚 [Gemini API Documentation](https://ai.google.dev/docs)
- 🔑 [Get API Key](https://makersuite.google.com/app/apikey)
- 💬 [Gemini Examples](https://ai.google.dev/examples)
- 🎓 [Prompt Engineering Guide](https://ai.google.dev/docs/prompt_best_practices)

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Google AI Documentation](https://ai.google.dev/docs)
3. Open an issue on GitHub
4. Contact support

---

**Happy AI-powered development with NEO! 🤖✨**
