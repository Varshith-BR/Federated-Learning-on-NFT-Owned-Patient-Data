
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import hashlib
from datetime import datetime, timedelta
import sqlite3
import threading
import time
import time
import os
from blockchain_nft_system import NFTConsentManager
from blockchain_nft_system import NFTConsentManager

app = Flask(__name__)
CORS(app)

# Global variables for federated learning
global_model_state = {
    'accuracy': 0.0,
    'loss': 1.0,
    'round': 0,
    'participating_nodes': 0,
    'total_consented_data': 0
}

training_status = {
    'is_training': False,
    'current_round': 0,
    'total_rounds': 0,
    'progress': 0
}

class FederatedLearningEngine:
    """Federated Learning Engine for healthcare data with NFT consent"""

    def __init__(self):
        self.nodes = {}
        self.global_model = None
        self.training_history = []

    def register_node(self, node_id, hospital_name, data_path):
        """Register a hospital node for federated learning"""
        try:
            data = pd.read_csv(data_path)
            self.nodes[node_id] = {
                'hospital_name': hospital_name,
                'data': data,
                'status': 'active',
                'last_update': datetime.now()
            }
            return True
        except Exception as e:
            print(f"Error registering node {node_id}: {str(e)}")
            return False

    def apply_consent_filter(self, data):
        """Apply consent filtering as per Equation 3.1: D_filtered = {xi ∈ D : xi.allow_training = true}"""
        if 'allow_training' not in data.columns:
            return data  # If no consent column, use all data

        # Filter for consented data
        consented_data = data[data['allow_training'] == True].copy()

        # Check for expired consent
        if 'expiry_date' in consented_data.columns:
            current_date = datetime.now()
            unexpired_mask = (consented_data['expiry_date'].isna()) | (pd.to_datetime(consented_data['expiry_date'], errors='coerce') > current_date)
            consented_data = consented_data[unexpired_mask]

        return consented_data

    def simulate_local_training(self, node_data):
        """Simulate local model training on consented data"""
        # Apply consent filter
        filtered_data = self.apply_consent_filter(node_data)

        if len(filtered_data) == 0:
            return None, 0

        # Simulate training metrics
        accuracy = np.random.normal(0.85, 0.05)
        loss = np.random.normal(0.25, 0.05)

        return {
            'accuracy': max(0.5, min(0.99, accuracy)),
            'loss': max(0.01, loss),
            'data_points': len(filtered_data)
        }, len(filtered_data)

    def federated_training_round(self):
        """Execute one round of federated training"""
        participating_nodes = 0
        total_consented_data = 0
        local_accuracies = []
        local_losses = []

        for node_id, node_info in self.nodes.items():
            metrics, data_count = self.simulate_local_training(node_info['data'])

            if metrics:
                participating_nodes += 1
                total_consented_data += data_count
                local_accuracies.append(metrics['accuracy'])
                local_losses.append(metrics['loss'])

        # Global model aggregation
        if local_accuracies:
            global_accuracy = np.mean(local_accuracies)
            global_loss = np.mean(local_losses)
        else:
            global_accuracy = 0.0
            global_loss = float('inf')

        # Update global state
        global global_model_state
        global_model_state.update({
            'accuracy': global_accuracy,
            'loss': global_loss,
            'round': global_model_state['round'] + 1,
            'participating_nodes': participating_nodes,
            'total_consented_data': total_consented_data
        })

        round_result = {
            'round': global_model_state['round'],
            'global_accuracy': global_accuracy,
            'global_loss': global_loss,
            'participating_nodes': participating_nodes,
            'total_nodes': len(self.nodes),
            'total_consented_data': total_consented_data,
            'timestamp': datetime.now().isoformat()
        }

        self.training_history.append(round_result)
        return round_result

# Initialize FL Engine
fl_engine = FederatedLearningEngine()
nft_manager = NFTConsentManager()

# Load initial data if available
def load_initial_data():
    """Load hospital datasets and NFT metadata"""
    # Load blockchain state from CSV
    if os.path.exists('patient_dataset.csv') and os.path.exists('nft_metadata.csv'):
        print("Initializing blockchain from legacy CSVs...")
        count = nft_manager.initialize_from_csv_data('patient_dataset.csv', 'nft_metadata.csv')
        print(f"Restored {count} NFTs to blockchain")

    hospital_files = [
        ('node_metro_general', 'Metro General Hospital', 'node_metro_general_hospit_filtered_data.csv'),
        ('node_regional', 'Regional Healthcare System', 'node_regional_healthcare__filtered_data.csv'),
        ('node_st_marys', 'St. Mary\'s Hospital', 'node_st._marys_hospital_filtered_data.csv'),
        ('node_university', 'University Medical Center', 'node_university_medical_c_filtered_data.csv'),
        ('node_community', 'Community Health Network', 'node_community_health_net_filtered_data.csv'),
        ('node_city', 'City Medical Center', 'node_city_medical_center_filtered_data.csv'),
        ('node_veterans', 'Veterans Affairs Hospital', 'node_veterans_affairs_hos_data.csv'),
        ('node_childrens', 'Children\'s Medical Center', 'node_childrens_medical_ce_filtered_data.csv')
    ]

    for node_id, hospital_name, file_path in hospital_files:
        if os.path.exists(file_path):
            fl_engine.register_node(node_id, hospital_name, file_path)

    print(f"Loaded {len(fl_engine.nodes)} hospital nodes")

# Routes
@app.route('/')
def home():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/patient')
def patient_portal():
    """Patient consent management portal"""
    return render_template('patient_portal.html')

@app.route('/hospital')
def hospital_portal():
    """Hospital data management portal"""
    return render_template('hospital_portal.html')

@app.route('/training')
def training_dashboard():
    """Federated learning training dashboard"""
    return render_template('training_dashboard.html')

@app.route('/api/nodes')
def get_nodes():
    """Get list of registered hospital nodes with live statistics from CSVs"""
    try:
        # Load fresh data from Source of Truth
        patient_data = pd.read_csv('patient_dataset.csv')
        nft_metadata = pd.read_csv('nft_metadata.csv')
        
        # Drop 'allow_training' from patient_data if it exists to avoid _x/_y suffixes
        if 'allow_training' in patient_data.columns:
            patient_data = patient_data.drop(columns=['allow_training'])

        # Merge to get allow_training status for all patients
        merged = patient_data.merge(nft_metadata[['patient_id', 'allow_training']], on='patient_id', how='left')
        merged['allow_training'] = merged['allow_training'].fillna(False)

        # Group by hospital
        hospital_stats = merged.groupby('hospital').agg(
            total_patients=('patient_id', 'count'),
            consented_patients=('allow_training', 'sum')
        ).reset_index()

        nodes_info = []
        
        # Map back to node architecture if needed, or just return hospital list
        # We'll try to preserve the existing structure but use fresh numbers
        # Re-using the hospital_files map from startup might be cleaner, but iterating the groupby is robust
        
        # We need to map hospital name -> node_id to match frontend expectation
        # Let's create a reverse mapping from the loaded nodes or just generate simple ones
        
        for index, row in hospital_stats.iterrows():
            hospital_name = row['hospital']
            # Find matching node_id from loaded engine or generate one
            node_id = "unknown"
            status = "active"
            
            # Try to find in existing engine to get the correct node_id (e.g. node_metro_general)
            for nid, ninfo in fl_engine.nodes.items():
                if ninfo['hospital_name'] == hospital_name:
                    node_id = nid
                    status = ninfo['status']
                    break
            
            if node_id == "unknown":
                # Fallback if not in engine (shouldn't happen)
                node_id = f"node_{hospital_name.lower().replace(' ', '_')}"

            nodes_info.append({
                'node_id': node_id,
                'hospital_name': hospital_name,
                'total_patients': int(row['total_patients']),
                'consented_patients': int(row['consented_patients']),
                'consent_rate': (row['consented_patients'] / row['total_patients'] * 100) if row['total_patients'] > 0 else 0,
                'status': status
            })

        return jsonify(nodes_info)

    except Exception as e:
        print(f"Error in get_nodes: {e}")
        return jsonify([])

@app.route('/api/global_model')
def get_global_model_state():
    """Get current global model state"""
    return jsonify(global_model_state)

@app.route('/api/training_history')
def get_training_history():
    """Get federated learning training history"""
    return jsonify(fl_engine.training_history)

@app.route('/api/start_training', methods=['POST'])
def start_training():
    """Start federated learning training"""
    global training_status

    data = request.json
    num_rounds = data.get('rounds', 3)

    if training_status['is_training']:
        return jsonify({'error': 'Training already in progress'}), 400

    training_status.update({
        'is_training': True,
        'current_round': 0,
        'total_rounds': num_rounds,
        'progress': 0
    })

    def training_thread():
        global training_status
        for round_num in range(num_rounds):
            training_status['current_round'] = round_num + 1
            training_status['progress'] = ((round_num + 1) / num_rounds) * 100

            result = fl_engine.federated_training_round()
            time.sleep(2)  # Simulate training time

        training_status['is_training'] = False
        training_status['progress'] = 100

    thread = threading.Thread(target=training_thread)
    thread.start()

    return jsonify({'message': 'Training started', 'rounds': num_rounds})

@app.route('/api/training_status')
def get_training_status():
    """Get current training status"""
    return jsonify(training_status)

@app.route('/blockchain')
def blockchain_explorer():
    """View blockchain explorer"""
    return render_template('blockchain_explorer.html')

@app.route('/api/blockchain')
def get_blockchain_data():
    """Get blockchain data (limited to last 50 blocks for performance)"""
    # Performance Optimization: Only send the last 50 blocks to the client
    # Sending 700+ blocks crashes the JSON serializer and browser
    limit = 50
    full_chain = nft_manager.blockchain.chain
    
    # Get last N blocks
    recent_blocks = full_chain[-limit:] if len(full_chain) > limit else full_chain
    chain_data = [block.to_dict() for block in recent_blocks]
    
    return jsonify({
        'chain': chain_data,
        'length': len(full_chain), # Send total length for stats
        'valid': nft_manager.blockchain.is_chain_valid()
    })

@app.route('/api/patients')
def get_patients():
    """Get patient data with consent information"""
    try:
        # Load patient data and NFT metadata
        patient_data = pd.read_csv('patient_dataset.csv')
        nft_metadata = pd.read_csv('nft_metadata.csv')

        # Drop overlapping columns from patient_data (preferring fresh data from nft_metadata)
        cols_to_drop = ['wallet_id', 'allow_training', 'consent_timestamp', 'expiry_date', 'data_hash']
        patient_data = patient_data.drop(columns=[c for c in cols_to_drop if c in patient_data.columns])

        # Merge patient data with NFT metadata
        merged_data = patient_data.merge(nft_metadata[['patient_id', 'wallet_id', 'allow_training', 'consent_timestamp', 'expiry_date']], 
                                        on='patient_id', how='left')

        # Fill NaN values for allow_training with False (default)
        merged_data['allow_training'] = merged_data['allow_training'].fillna(False)

        # Server-side Filtering: Check if hospital is requested
        hospital_filter = request.args.get('hospital')
        if hospital_filter:
            merged_data = merged_data[merged_data['hospital'] == hospital_filter]
        
        # Convert to JSON (handling NaNs -> null for valid JSON)
        patients = merged_data.replace({np.nan: None}).to_dict('records')

        # Only limit if getting ALL patients (to prevent crash), 
        # but if filtered by hospital, return all matching patients
        if not hospital_filter:
             # Increase limit slightly or implement pagination if needed
             # For now, return top 200 to keep dashboard responsive
             return jsonify(patients[:200])
        
        return jsonify(patients)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/api/update_consent', methods=['POST'])
def update_patient_consent():
    """Update patient consent status"""
    data = request.json
    patient_id = data.get('patient_id')
    allow_training = data.get('allow_training')
    expiry_date = data.get('expiry_date')
    wallet_address = data.get('wallet_address') # New

    try:
        # Load NFT metadata
        nft_metadata = pd.read_csv('nft_metadata.csv')

        # Update consent
        mask = nft_metadata['patient_id'] == patient_id
        nft_metadata.loc[mask, 'allow_training'] = allow_training
        nft_metadata.loc[mask, 'consent_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if wallet_address:
            nft_metadata.loc[mask, 'wallet_id'] = wallet_address

        if expiry_date:
            nft_metadata.loc[mask, 'expiry_date'] = expiry_date
        
        # Save updated metadata
        nft_metadata.to_csv('nft_metadata.csv', index=False)

        # Update hospital datasets
        hospital_files = [
            'node_metro_general_hospit_filtered_data.csv',
            'node_regional_healthcare__filtered_data.csv',
            'node_st._marys_hospital_filtered_data.csv',
            'node_university_medical_c_filtered_data.csv',
            'node_community_health_net_filtered_data.csv',
            'node_city_medical_center_filtered_data.csv',
            'node_veterans_affairs_hos_filtered_data.csv',
            'node_childrens_medical_ce_filtered_data.csv'
        ]

        for file_path in hospital_files:
            if os.path.exists(file_path):
                hospital_data = pd.read_csv(file_path)
                if patient_id in hospital_data['patient_id'].values:
                    hospital_data.loc[hospital_data['patient_id'] == patient_id, 'allow_training'] = allow_training
                    if expiry_date:
                        hospital_data.loc[hospital_data['patient_id'] == patient_id, 'expiry_date'] = expiry_date
                    hospital_data.to_csv(file_path, index=False)

                    # Re-register the node with updated data
                    node_id = file_path.split('_')[1] + '_' + file_path.split('_')[2]
                    if node_id in fl_engine.nodes:
                        fl_engine.nodes[node_id]['data'] = hospital_data

        return jsonify({'message': 'Consent updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/api/consent_analytics')
def get_consent_analytics():
    """Get consent analytics and statistics"""
    try:
        nft_metadata = pd.read_csv('nft_metadata.csv')
        patient_data = pd.read_csv('patient_dataset.csv')

        # Overall statistics
        total_patients = len(nft_metadata)
        consented_patients = nft_metadata['allow_training'].sum()
        consent_rate = (consented_patients / total_patients * 100) if total_patients > 0 else 0

        # Hospital-wise statistics
        hospital_stats = []
        for hospital in patient_data['hospital'].unique():
            hospital_patients = patient_data[patient_data['hospital'] == hospital]['patient_id']
            hospital_metadata = nft_metadata[nft_metadata['patient_id'].isin(hospital_patients)]

            hospital_consented = hospital_metadata['allow_training'].sum()
            hospital_total = len(hospital_metadata)

            hospital_stats.append({
                'hospital': hospital,
                'total_patients': hospital_total,
                'consented_patients': hospital_consented,
                'consent_rate': (hospital_consented / hospital_total * 100) if hospital_total > 0 else 0
            })

        # Age group analysis
        merged_data = patient_data.merge(nft_metadata[['patient_id', 'allow_training']], on='patient_id')
        merged_data['age_group'] = pd.cut(merged_data['age'], 
                                         bins=[0, 18, 30, 45, 60, 75, 100], 
                                         labels=['0-18', '19-30', '31-45', '46-60', '61-75', '75+'])

        age_stats = merged_data.groupby('age_group')['allow_training'].agg(['count', 'sum']).reset_index()
        age_stats['consent_rate'] = (age_stats['sum'] / age_stats['count'] * 100)
        age_stats = age_stats.to_dict('records')

        return jsonify({
            'overview': {
                'total_patients': total_patients,
                'consented_patients': consented_patients,
                'consent_rate': consent_rate
            },
            'hospital_stats': hospital_stats,
            'age_stats': age_stats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    # Load initial data
    load_initial_data()

    import socket
    def get_local_ip():
        try:
            # Connect to an external server (doesn't actually send data) to get the interface IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"

    local_ip = get_local_ip()

    print("\n" + "="*60)
    print("BLOCKCHAIN INITIALIZATION COMPLETE")
    print("="*60)
    print("Flask Server Starting IPConfig...")
    print(f"Local Access:   http://localhost:5000")
    print(f"Mobile/LAN:     http://{local_ip}:5000")
    print("="*60 + "\n")

    # Start the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
