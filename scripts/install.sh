#!/bin/bash

# NEO Installation Script

echo "========================================="
echo "Installing NEO: Neural Executive Operator"
echo "========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Detected Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install NEO in development mode
echo "Installing NEO..."
pip install -e .

# Create necessary directories
echo "Creating directories..."
mkdir -p logs models data

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

echo "========================================="
echo "Installation complete!"
echo "========================================="
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start NEO, run:"
echo "  python -m src.main --mode interactive"
echo ""
echo "Or simply:"
echo "  neo"
echo ""
