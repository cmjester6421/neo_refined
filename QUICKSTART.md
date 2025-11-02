# NEO Quick Start Guide

## 5-Minute Setup

Get NEO up and running in just 5 minutes!

### Step 1: Install (1 minute)

```bash
# Clone and navigate to NEO
git clone https://github.com/yourusername/neo.git
cd neo

# Run installation
chmod +x scripts/install.sh
./scripts/install.sh
```

### Step 2: Activate Environment (10 seconds)

```bash
source venv/bin/activate
```

### Step 3: Run NEO (30 seconds)

```bash
# Start NEO in interactive mode
python -m src.main --mode interactive
```

### Step 4: Try Some Commands (3 minutes)

```
You: Hello NEO
NEO: Hello! I'm NEO, your Neural Executive Operator. How can I assist you today?

You: Show me system information
NEO: System: Linux 5.15.0, CPU: 25.3%, Memory: 45.2%

You: Generate a secure password
NEO: Generated secure password: X9#mK2$pL5@nQ8

You: What is artificial intelligence?
NEO: That's an interesting question...
```

## Common Commands

### System Information
```
system info
show processes
monitor cpu
```

### Security
```
generate password
check password MyP@ssw0rd
```

### Coding
```
analyze code
help with Python
```

### Research
```
research machine learning
find information about Python
```

### Help
```
help
status
```

### Exit
```
exit
quit
bye
```

## Next Steps

1. **Read the Full Guide**: Check out [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
2. **Configure NEO**: Edit `config/neo_config.yaml`
3. **Explore Features**: Try different modules
4. **Join Community**: Contribute on GitHub

## Troubleshooting

### Problem: Import errors
**Solution**: 
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: Permission denied
**Solution**:
```bash
chmod +x scripts/*.sh
```

### Problem: Python version error
**Solution**: NEO requires Python 3.8+
```bash
python --version  # Should be 3.8 or higher
```

## Using Docker (Alternative)

If you prefer Docker:

```bash
# Build and run
docker-compose up -d

# Access NEO
docker exec -it neo-assistant python -m src.main
```

## Get Help

- 📖 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/neo/issues)
- 💬 [Discussions](https://github.com/yourusername/neo/discussions)

---

**You're all set! Enjoy using NEO!** 🔹
