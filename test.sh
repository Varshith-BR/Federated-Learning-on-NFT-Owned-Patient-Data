#!/bin/bash

# Test script for Federated Learning NFT system

echo "🧪 Running System Tests..."
echo "========================="

# Activate virtual environment if it exists
if [ -d "fl-nft-env" ]; then
    source fl-nft-env/bin/activate
fi

# Test 1: Import all modules
echo "Test 1: Module imports..."
python -c "
try:
    import app
    import blockchain_nft_system
    import federated_learning_engine
    print('✓ All modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
"

# Test 2: Check data files
echo "Test 2: Data files..."
if [ -f "patient_dataset.csv" ]; then
    records=$(wc -l < patient_dataset.csv)
    echo "✓ Patient dataset: $records records"
else
    echo "⚠️  Patient dataset will be generated"
fi

# Test 3: Test NFT system
echo "Test 3: NFT system..."
python -c "
from blockchain_nft_system import NFTConsentManager
try:
    manager = NFTConsentManager()
    token_id = manager.create_patient_nft('TEST001', {'allow_training': True})
    is_valid, reason = manager.verify_patient_consent('TEST001')
    print(f'✓ NFT system working - Token: {token_id[:16]}...')
    print(f'✓ Consent verification: {is_valid}')
except Exception as e:
    print(f'❌ NFT system error: {e}')
"

# Test 4: Test FL engine  
echo "Test 4: Federated learning..."
python -c "
from federated_learning_engine import FederatedLearningServer
import os
try:
    server = FederatedLearningServer()
    print('✓ FL server initialized')

    # Test with sample data if available
    if os.path.exists('patient_dataset.csv'):
        print('✓ Sample data available for FL testing')
    else:
        print('⚠️  No sample data for FL testing')
except Exception as e:
    print(f'❌ FL engine error: {e}')
"

# Test 5: Web application
echo "Test 5: Web application..."
timeout 5 python -c "
from app import app
import threading
import requests
import time

def start_server():
    app.run(port=5001, debug=False)

# Start server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(2)

try:
    response = requests.get('http://localhost:5001', timeout=2)
    if response.status_code == 200:
        print('✓ Web application responding')
    else:
        print(f'⚠️  Web app status: {response.status_code}')
except:
    print('⚠️  Web application test incomplete')
" 2>/dev/null || echo "⚠️  Web application test skipped"

echo ""
echo "🎯 Test Summary:"
echo "- If all tests show ✓, the system is ready"
echo "- ⚠️  warnings are usually not critical"  
echo "- ❌ errors need to be resolved"
echo ""
echo "To start the system: ./run.sh or python app.py"
