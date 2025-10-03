#!/bin/bash

# Research Hub - Quick Start Script

echo "🔬 Research Hub - Multi-Agent Framework"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please add your ANTHROPIC_API_KEY to .env"
    echo ""
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
source .env
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set in .env file"
    echo "Please add your API key to .env"
    exit 1
fi

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Run the Streamlit app
echo "🚀 Starting Research Hub frontend..."
echo "Open your browser to: http://localhost:8501"
echo ""
streamlit run frontend/app.py
