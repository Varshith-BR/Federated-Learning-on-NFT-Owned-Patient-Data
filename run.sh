#!/bin/bash

# Quick run script for Federated Learning NFT system

echo "🚀 Starting Federated Learning NFT Healthcare System..."

# Activate virtual environment if it exists
if [ -d "fl-nft-env" ]; then
    source fl-nft-env/bin/activate
    echo "✓ Virtual environment activated"
fi

# Check if required files exist
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please ensure all files are in the current directory."
    exit 1
fi

# Set environment variables for development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start the application
echo "🌟 Launching web application on http://localhost:5000"
echo "🔑 Press Ctrl+C to stop the server"
echo ""

python app.py
