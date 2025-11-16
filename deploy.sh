#!/bin/bash

# Deployment script for Road Safety RAG Application

echo "🚀 Road Safety RAG Deployment Script"
echo "======================================"

# Check if running in correct directory
if [ ! -f "web_interface.py" ]; then
    echo "❌ Error: web_interface.py not found. Please run from project root."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_complete.txt

# Verify setup
echo "🔍 Verifying setup..."
python verify_setup.py

# Check if interventions.json exists
if [ ! -f "interventions.json" ]; then
    echo "⚠️  Warning: interventions.json not found"
fi

# Check Ollama
echo "🔍 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    ollama list
else
    echo "⚠️  Ollama not found. Install from https://ollama.ai"
fi

# Start application
echo "🚀 Starting Streamlit application..."
echo "Access at: http://localhost:8501"
streamlit run web_interface.py --server.port=8501 --server.address=0.0.0.0

