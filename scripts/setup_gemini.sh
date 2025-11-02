#!/bin/bash

# Gemini AI Setup Script for NEO
echo "🤖 Gemini AI Setup for NEO"
echo "=========================="
echo ""

# Check if running in virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: Not running in a virtual environment"
    echo "It's recommended to activate the virtual environment first:"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install google-generativeai package
echo "📦 Installing google-generativeai package..."
pip install google-generativeai

if [ $? -ne 0 ]; then
    echo "❌ Failed to install google-generativeai"
    exit 1
fi

echo "✅ google-generativeai installed successfully"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "🔑 Gemini API Key Setup"
echo "----------------------"
echo "To use Gemini AI, you need a Google API key."
echo ""
echo "Get your API key from: https://makersuite.google.com/app/apikey"
echo ""
read -p "Do you have a Gemini API key? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Enter your Gemini API key: " api_key
    
    if [ -n "$api_key" ]; then
        # Update .env file
        if grep -q "GEMINI_API_KEY=" .env; then
            # Replace existing key
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s|GEMINI_API_KEY=.*|GEMINI_API_KEY=$api_key|" .env
            else
                # Linux
                sed -i "s|GEMINI_API_KEY=.*|GEMINI_API_KEY=$api_key|" .env
            fi
        else
            # Add new key
            echo "GEMINI_API_KEY=$api_key" >> .env
        fi
        
        echo "✅ API key saved to .env file"
    else
        echo "⚠️  No API key provided"
    fi
else
    echo ""
    echo "ℹ️  You can add your API key later by editing the .env file:"
    echo "   GEMINI_API_KEY=your_api_key_here"
fi

echo ""
echo "✅ Gemini AI setup complete!"
echo ""
echo "Next steps:"
echo "1. If you haven't added your API key, edit .env and add:"
echo "   GEMINI_API_KEY=your_api_key_here"
echo "2. Run NEO: python -m src.main"
echo "3. Try Gemini commands:"
echo "   - /ai What is artificial intelligence?"
echo "   - /code <paste your code>"
echo "   - /solve How to optimize a binary search?"
echo ""
echo "For more info: https://ai.google.dev/docs"
echo ""
