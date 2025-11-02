#!/bin/bash

# Run NEO Tests

echo "Running NEO Test Suite..."
echo "=========================="

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

echo ""
echo "Test coverage report generated in htmlcov/index.html"
