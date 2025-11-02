# NEO Installation & Verification Guide

## Pre-Installation Checklist

Before installing NEO, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] pip package manager installed
- [ ] Git installed (for cloning)
- [ ] At least 500MB free disk space
- [ ] Internet connection for downloading dependencies

## Installation Steps

### Method 1: Automated Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/neo.git
cd neo

# 2. Run the installation script
chmod +x scripts/install.sh
./scripts/install.sh

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Verify installation
python -c "from src.main import NEOAssistant; print('✅ NEO installed successfully!')"
```

### Method 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/neo.git
cd neo

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install NEO in development mode
pip install -e .

# 7. Create necessary directories
mkdir -p logs models data

# 8. Copy environment file
cp .env.example .env
```

### Method 3: Docker Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/neo.git
cd neo

# 2. Build and start containers
docker-compose up -d

# 3. Verify installation
docker exec neo-assistant python -c "from src.main import NEOAssistant; print('✅ NEO installed!')"
```

## Verification Steps

### Step 1: Verify Python Version

```bash
python --version
# Should output: Python 3.8.x or higher
```

### Step 2: Verify Dependencies

```bash
pip list | grep -E "torch|transformers|fastapi"
# Should show installed packages
```

### Step 3: Test Module Imports

```bash
python << EOF
from src.core.ai_engine import NEOAIEngine
from src.modules.system_control import SystemControl
from src.modules.cybersecurity import CybersecurityModule
from src.modules.coding_assistant import CodingAssistant
from src.modules.research import ResearchModule
from src.modules.task_automation import TaskAutomation
from src.modules.nlp_conversation import NLPConversation
print("✅ All modules imported successfully!")
EOF
```

### Step 4: Run Tests

```bash
# Run basic tests
python -m pytest tests/test_ai_engine.py -v

# Run all tests
./scripts/test.sh
```

### Step 5: Start NEO

```bash
# Interactive mode
python -m src.main --mode interactive

# Or simply
neo
```

## Expected Output

When you start NEO, you should see:

```
============================================================
Initializing NEO v1.0.0
============================================================
2025-11-02 10:00:00 - NEO - INFO - Loading AI Engine...
2025-11-02 10:00:01 - NEO - INFO - Loading System Control...
2025-11-02 10:00:01 - NEO - INFO - Loading Cybersecurity Module...
2025-11-02 10:00:01 - NEO - INFO - Loading Coding Assistant...
2025-11-02 10:00:01 - NEO - INFO - Loading Research Module...
2025-11-02 10:00:01 - NEO - INFO - Loading Task Automation...
2025-11-02 10:00:01 - NEO - INFO - Loading NLP Conversation...
2025-11-02 10:00:02 - NEO - INFO - ✓ All modules loaded successfully
============================================================

============================================================
🔹 NEO - Neural Executive Operator
Version: 1.0.0
============================================================

Type 'help' for available commands, 'exit' to quit.

You: 
```

## Troubleshooting

### Issue: "No module named 'schedule'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Permission denied"

**Solution**: Make scripts executable
```bash
chmod +x scripts/*.sh
```

### Issue: Python version too old

**Solution**: Install Python 3.8+
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3.8

# On macOS
brew install python@3.8

# On Windows
# Download from python.org
```

### Issue: "pip: command not found"

**Solution**: Install pip
```bash
python3 -m ensurepip --upgrade
```

### Issue: Virtual environment activation fails

**Solution**: Different activation for different shells
```bash
# Bash/Zsh
source venv/bin/activate

# Fish
source venv/bin/activate.fish

# Windows CMD
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1
```

## Post-Installation Configuration

### 1. Environment Variables

Edit `.env` file:
```bash
NEO_ENV=development
NEO_DEBUG=true
NEO_BASE_DIR=/path/to/neo

# Optional API keys for enhanced features
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

### 2. Configuration File

Edit `config/neo_config.yaml`:
```yaml
ai:
  learning_rate: 0.001
  confidence_threshold: 0.8

system:
  enable_shutdown: false  # Keep false for safety
  max_retries: 3
```

### 3. Logging Level

Adjust in `config/neo_config.yaml`:
```yaml
logging:
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  log_dir: "logs"
```

## Verification Checklist

After installation, verify:

- [ ] Python version is 3.8+
- [ ] Virtual environment is activated
- [ ] All dependencies are installed
- [ ] All modules import without errors
- [ ] Tests pass successfully
- [ ] NEO starts without errors
- [ ] Configuration files are present
- [ ] Logs directory is created
- [ ] Can execute basic commands
- [ ] Help command works

## Quick Test Commands

Once NEO is running, test these commands:

```
help                    # Show available commands
status                  # Check NEO status
system info            # Get system information
generate password      # Generate secure password
exit                   # Exit NEO
```

## Performance Notes

### First Run
- First run may take 10-30 seconds to initialize all modules
- AI models are loaded into memory
- Subsequent runs will be faster

### Resource Usage
- **Memory**: ~200-500 MB (depending on loaded models)
- **Disk**: ~500 MB (with dependencies)
- **CPU**: Minimal when idle, higher during AI processing

## Getting Help

If you encounter issues:

1. Check logs in `logs/` directory
2. Enable debug mode: `NEO_DEBUG=true`
3. Check [GitHub Issues](https://github.com/yourusername/neo/issues)
4. Read [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
5. Review [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

## Next Steps

After successful installation:

1. ✅ Read the [User Guide](docs/USER_GUIDE.md)
2. ✅ Try example commands
3. ✅ Explore different modules
4. ✅ Configure to your needs
5. ✅ Join the community and contribute!

---

**Congratulations! You've successfully installed NEO!** 🎉🔹
