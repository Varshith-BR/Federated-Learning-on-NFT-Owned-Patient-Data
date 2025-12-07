#!/bin/bash

# Federated Learning on NFT-Owned Patient Data
# Automatic Installation Script

echo "🚀 Installing Federated Learning NFT Healthcare System"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install Python pip first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv fl-nft-env
source fl-nft-env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Verify installation
echo "✅ Verifying installation..."
python -c "import flask, pandas, sklearn, numpy; print('All packages installed successfully!')"

# Check data files
echo "📊 Checking data files..."
if [ -f "patient_dataset.csv" ]; then
    echo "✓ Patient dataset found"
else
    echo "⚠️  Patient dataset not found - will be generated on first run"
fi

# Make scripts executable
chmod +x run.sh
chmod +x test.sh

echo "🎉 Installation completed successfully!"
echo ""
echo "To start the system:"
echo "1. Activate environment: source fl-nft-env/bin/activate"  
echo "2. Run application: python app.py"
echo "3. Open browser: http://localhost:5000"
echo ""
echo "For help, see README.md"
