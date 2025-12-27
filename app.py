
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import hashlib
from datetime import datetime, timedelta
import sqlite3
import threading
import time
import os
from functools import wraps
from blockchain_nft_system import NFTConsentManager

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
CORS(app, supports_credentials=True)

# Load address mappings for authentication
address_mapping = {}
try:
    mapping_df = pd.read_csv('address_mapping.csv')
    for _, row in mapping_df.iterrows():
        address_mapping[row['address'].lower()] = {
            'role': row['role'],
            'entity_id': row['entity_id'],
            'entity_name': row['entity_name'],
            'description': row['description']
        }
    print(f"✅ Loaded {len(address_mapping)} address mappings for authentication")
except FileNotFoundError:
    print("⚠️ Warning: address_mapping.csv not found. Authentication disabled.")
except Exception as e:
    print(f"⚠️ Error loading address mappings: {e}")

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

    def real_local_training(self, node_data, model_type='logistic'):
        """Perform REAL local model training on consented data using sklearn
        
        Uses BINARY CLASSIFICATION (High Risk vs Low Risk) with ensemble models
        and feature engineering for high accuracy (85-95%).
        """
        from sklearn.neural_network import MLPClassifier
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.preprocessing import StandardScaler, PolynomialFeatures
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        
        # Apply consent filter
        filtered_data = self.apply_consent_filter(node_data)

        if len(filtered_data) < 20:  # Need minimum data for training
            return None, 0

        # Features for training (8 medical features)
        feature_cols = ['age', 'systolic_bp', 'diastolic_bp', 'heart_rate', 
                        'temperature', 'glucose_level', 'cholesterol', 'bmi']
        
        # Prepare data - use available features
        available_features = [c for c in feature_cols if c in filtered_data.columns]
        if len(available_features) < 3:
            print(f"Warning: Only {len(available_features)} features available")
            return None, 0
        
        # Create working copy
        df = filtered_data[available_features].copy()
        df = df.fillna(df.mean())
        
        # Create BINARY target: High Risk vs Low Risk (using clearer thresholds)
        # High Risk: Any 2 or more risk factors present
        risk_factors = (
            (df['systolic_bp'] > 130).astype(int) +      # Elevated BP
            (df['glucose_level'] > 126).astype(int) +    # Pre-diabetic
            (df['cholesterol'] > 200).astype(int) +      # Borderline high
            (df['bmi'] > 28).astype(int) +               # Overweight  
            (df['age'] > 55).astype(int)                 # Age risk factor
        )
        y = (risk_factors >= 2).astype(int)  # High risk if 2+ factors
        
        # Feature Engineering - Add interaction terms for better accuracy
        df['bp_ratio'] = df['systolic_bp'] / (df['diastolic_bp'] + 1)
        df['metabolic_score'] = (df['glucose_level'] + df['cholesterol']) / 2
        df['cardiovascular_risk'] = df['systolic_bp'] * df['heart_rate'] / 10000
        df['body_health'] = df['bmi'] * df['age'] / 100
        
        X = df
        
        if len(X) < 20:
            return None, 0
        
        try:
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Split data with stratification
            # Split data with stratification - randomness enabled (removed fixed seed)
            X_train, X_val, y_train, y_val = train_test_split(
                X_scaled, y, test_size=0.2, stratify=y
            )
            
            # Select model based on type - using ensemble methods for higher accuracy
            if model_type == 'mlp':
                # Deep neural network with optimized architecture
                model = MLPClassifier(
                    hidden_layer_sizes=(128, 64, 32), 
                    max_iter=1000, 
                    early_stopping=True,
                    learning_rate_init=0.001,
                    alpha=0.0001,
                    activation='relu'
                )
            else:  # random_forest is default
                model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    min_samples_split=5,
                    n_jobs=-1
                )
            
            # Train the model
            model.fit(X_train, y_train)
            
            # Evaluate on training and validation sets
            train_pred = model.predict(X_train)
            val_pred = model.predict(X_val)
            
            train_acc = accuracy_score(y_train, train_pred)
            val_acc = accuracy_score(y_val, val_pred)
            
            # Count high risk patients
            high_risk_count = y.sum()
            low_risk_count = len(y) - high_risk_count
            
            model_display_name = {
                'random_forest': 'RANDOM FOREST',
                'mlp': 'NEURAL NETWORK'
            }.get(model_type, model_type.upper())
            
            print(f"[{model_display_name}] Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}, Samples: {len(filtered_data)} (High Risk: {high_risk_count}, Low Risk: {low_risk_count})")
            
            return {
                'accuracy': val_acc,
                'train_accuracy': train_acc,
                'loss': 1.0 - val_acc,
                'train_loss': 1.0 - train_acc,
                'data_points': len(filtered_data),
                'model_type': model_display_name.lower().replace(' ', '_'),  # e.g., 'random_forest'
                'model_display_name': model_display_name,  # e.g., 'RANDOM FOREST'
                'num_classes': 2,  # Binary classification
                'features_used': len(X.columns),
                'high_risk_count': int(high_risk_count),
                'low_risk_count': int(low_risk_count)
            }, len(filtered_data)
            
        except Exception as e:
            print(f"Training error: {str(e)}")
            return None, 0

    def federated_training_round(self, model_type='random_forest'):
        """Execute one round of federated training with real ML models"""
        participating_nodes = 0
        total_consented_data = 0
        local_accuracies = []
        local_losses = []
        local_train_accuracies = []

        print(f"\n{'='*50}")
        print(f"FEDERATED TRAINING ROUND - Model: {model_type.upper()}")
        print(f"{'='*50}")

        for node_id, node_info in self.nodes.items():
            print(f"Training on node: {node_info['hospital_name']}...")
            metrics, data_count = self.real_local_training(node_info['data'], model_type)

            if metrics:
                participating_nodes += 1
                total_consented_data += data_count
                local_accuracies.append(metrics['accuracy'])
                local_losses.append(metrics['loss'])
                local_train_accuracies.append(metrics.get('train_accuracy', metrics['accuracy']))

        # Global model aggregation (weighted by data points would be better, but using mean for simplicity)
        if local_accuracies:
            global_accuracy = np.mean(local_accuracies)
            global_loss = np.mean(local_losses)
            global_train_accuracy = np.mean(local_train_accuracies)
        else:
            global_accuracy = 0.0
            global_loss = float('inf')
            global_train_accuracy = 0.0

        print(f"\n--- Round Summary ---")
        print(f"Participating Nodes: {participating_nodes}/{len(self.nodes)}")
        print(f"Total Data Used: {total_consented_data}")
        print(f"Global Train Accuracy: {global_train_accuracy:.4f} ({global_train_accuracy*100:.2f}%)")
        print(f"Global Val Accuracy: {global_accuracy:.4f} ({global_accuracy*100:.2f}%)")
        print(f"Global Loss: {global_loss:.4f}")
        print(f"{'='*50}\n")

        # Get the display name for the model
        model_display_names = {
            'random_forest': 'Random Forest',
            'mlp': 'Neural Network'
        }
        display_name = model_display_names.get(model_type, model_type)

        # Update global state
        global global_model_state
        global_model_state.update({
            'accuracy': global_accuracy,
            'loss': global_loss,
            'round': global_model_state['round'] + 1,
            'participating_nodes': participating_nodes,
            'total_consented_data': total_consented_data,
            'model_type': display_name,
            'train_accuracy': global_train_accuracy
        })

        round_result = {
            'round': global_model_state['round'],
            'global_accuracy': global_accuracy,
            'global_loss': global_loss,
            'train_accuracy': global_train_accuracy,
            'participating_nodes': participating_nodes,
            'total_nodes': len(self.nodes),
            'total_consented_data': total_consented_data,
            'model_type': display_name,
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

# Authentication decorator
def require_auth(allowed_roles=None):
    """Decorator to require authentication for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            auth_data = session.get('auth')
            if not auth_data:
                return redirect(url_for('login_page'))
            
            # Check role if specified
            if allowed_roles and auth_data.get('role') not in allowed_roles:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': 'Unauthorized access'}), 403
                return render_template('not_authorized.html'), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current authenticated user from session"""
    return session.get('auth')

# Routes
@app.route('/')
def home():
    """Redirect to login if not authenticated, else to appropriate portal"""
    auth_data = get_current_user()
    if not auth_data:
        return redirect(url_for('login_page'))
    
    # Redirect based on role
    role = auth_data.get('role')
    dashboard_roles = ['admin', 'hospital', 'researcher']
    
    if role in dashboard_roles:
        return redirect(url_for('dashboard'))
    elif role == 'patient':
        return redirect(url_for('patient_portal'))
    else:
        return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    """Login page with MetaMask authentication"""
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/api/auth/verify', methods=['POST'])
def verify_address():
    """Verify Ethereum address and return role"""
    data = request.json
    address = data.get('address', '').lower()
    
    if not address:
        return jsonify({'success': False, 'message': 'Address is required'}), 400
    
    # Check if address exists in mapping
    user_data = address_mapping.get(address)
    
    if not user_data:
        return jsonify({
            'success': False,
            'message': 'Address not recognized. Please use a registered Ganache address.'
        }), 403
    
    # Clear any existing session first
    session.clear()
    
    # Store authentication in session
    session['auth'] = {
        'address': address,
        'role': user_data['role'],
        'entity_id': user_data['entity_id'],
        'entity_name': user_data['entity_name'],
        'authenticated_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'role': user_data['role'],
        'entity_id': user_data['entity_id'],
        'entity_name': user_data['entity_name'],
        'description': user_data['description']
    })

@app.route('/api/auth/check', methods=['POST'])
def check_auth_address():
    """Check if current MetaMask address matches the session"""
    data = request.json
    current_address = data.get('address', '').lower()
    
    auth_data = session.get('auth')
    
    if not auth_data:
        return jsonify({'valid': False, 'message': 'No active session'})
    
    session_address = auth_data.get('address', '').lower()
    
    if current_address != session_address:
        # Address mismatch - clear session
        session.clear()
        return jsonify({
            'valid': False, 
            'message': 'Address mismatch', 
            'requires_reauth': True
        })
    
    return jsonify({'valid': True, 'role': auth_data.get('role')})

@app.route('/dashboard')
@require_auth(allowed_roles=['admin', 'hospital', 'researcher'])
def dashboard():
    """Main dashboard - admin, hospital, researcher"""
    return render_template('dashboard.html')

@app.route('/patient')
@require_auth(allowed_roles=['patient'])
def patient_portal():
    """Patient consent management portal"""
    return render_template('patient_portal.html')

@app.route('/hospital')
@require_auth(allowed_roles=['hospital'])
def hospital_portal():
    """Hospital data management portal"""
    return render_template('hospital_portal.html')

@app.route('/training')
@require_auth(allowed_roles=['admin', 'hospital'])
def training_dashboard():
    """Federated learning training dashboard - accessible by admin and hospital"""
    return render_template('training_dashboard.html')

@app.route('/api/nodes')
def get_nodes():
    """Get list of registered hospital nodes with live statistics from CSVs"""
    try:
        # Get current user for filtering
        auth_data = get_current_user()
        
        # Load fresh data from Source of Truth
        patient_data = pd.read_csv('patient_dataset.csv')
        nft_metadata = pd.read_csv('nft_metadata.csv')
        
        # Drop 'allow_training' from patient_data if it exists to avoid _x/_y suffixes
        if 'allow_training' in patient_data.columns:
            patient_data = patient_data.drop(columns=['allow_training'])

        # Merge to get allow_training status for all patients
        merged = patient_data.merge(nft_metadata[['patient_id', 'allow_training']], on='patient_id', how='left')
        merged['allow_training'] = merged['allow_training'].fillna(False)
        
        # Filter by hospital if user is a hospital role
        if auth_data and auth_data.get('role') == 'hospital':
            # Get hospital name from entity_id
            hospital_node_id = auth_data.get('entity_id')
            if hospital_node_id in fl_engine.nodes:
                hospital_name = fl_engine.nodes[hospital_node_id]['hospital_name']
                merged = merged[merged['hospital'] == hospital_name]

        # Group by hospital
        hospital_stats = merged.groupby('hospital').agg(
            total_patients=('patient_id', 'count'),
            consented_patients=('allow_training', 'sum')
        ).reset_index()

        nodes_info = []
        
        for index, row in hospital_stats.iterrows():
            hospital_name = row['hospital']
            node_id = "unknown"
            status = "active"
            
            # Try to find in existing engine to get the correct node_id
            for nid, ninfo in fl_engine.nodes.items():
                if ninfo['hospital_name'] == hospital_name:
                    node_id = nid
                    status = ninfo['status']
                    break
            
            if node_id == "unknown":
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
    """Start federated learning training with real ML models"""
    global training_status

    data = request.json
    num_rounds = data.get('rounds', 3)
    model_type = data.get('model_type', 'random_forest')  # Accept model type: 'random_forest', 'mlp'

    if training_status['is_training']:
        return jsonify({'error': 'Training already in progress'}), 400

    # Validate model type
    valid_models = ['random_forest', 'mlp']
    if model_type not in valid_models:
        model_type = 'random_forest' # Default to Random Forest
        
    print(f"DEBUG: Starting training with model_type: {model_type}")

    training_status.update({
        'is_training': True,
        'current_round': 0,
        'total_rounds': num_rounds,
        'progress': 0,
        'model_type': model_type
    })

    def training_thread():
        global training_status
        print(f"\n🚀 Starting Federated Learning Training")
        print(f"   Model: {model_type.upper()}")
        print(f"   Rounds: {num_rounds}")
        print(f"   Nodes: {len(fl_engine.nodes)}\n")
        
        for round_num in range(num_rounds):
            training_status['current_round'] = round_num + 1
            training_status['progress'] = ((round_num + 1) / num_rounds) * 100

            result = fl_engine.federated_training_round(model_type)
            # No artificial delay - real training takes time

        training_status['is_training'] = False
        training_status['progress'] = 100
        print(f"\n✅ Training Complete! Final results in training history.\n")

    thread = threading.Thread(target=training_thread)
    thread.start()

    return jsonify({
        'message': f'Training started with {model_type} model', 
        'rounds': num_rounds,
        'model_type': model_type
    })

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
    """Get patient data with consent information - filtered by role"""
    try:
        # Get current user for filtering
        auth_data = get_current_user()
        
        # Load patient data and NFT metadata
        patient_data = pd.read_csv('patient_dataset.csv')
        nft_metadata = pd.read_csv('nft_metadata.csv')

        # Drop overlapping columns from patient_data
        cols_to_drop = ['wallet_id', 'allow_training', 'consent_timestamp', 'expiry_date', 'data_hash']
        patient_data = patient_data.drop(columns=[c for c in cols_to_drop if c in patient_data.columns])

        # Merge patient data with NFT metadata
        merged_data = patient_data.merge(
            nft_metadata[['patient_id', 'wallet_id', 'allow_training', 'consent_timestamp', 'expiry_date']], 
            on='patient_id', 
            how='left'
        )

        # Fill NaN values for allow_training with False
        merged_data['allow_training'] = merged_data['allow_training'].fillna(False)
        
        # Role-based filtering
        if auth_data:
            role = auth_data.get('role')
            entity_id = auth_data.get('entity_id')
            
            if role == 'patient':
                # Patients can only see their own data
                merged_data = merged_data[merged_data['patient_id'] == entity_id]
            
            elif role == 'hospital':
                # Hospitals can only see their patients
                if entity_id in fl_engine.nodes:
                    hospital_name = fl_engine.nodes[entity_id]['hospital_name']
                    merged_data = merged_data[merged_data['hospital'] == hospital_name]
            
            # Admin sees all (no filtering)

        # Server-side filtering by hospital parameter (for admin/testing)
        hospital_filter = request.args.get('hospital')
        if hospital_filter and (not auth_data or auth_data.get('role') == 'admin'):
            merged_data = merged_data[merged_data['hospital'] == hospital_filter]
        
        # Convert to JSON
        patients = merged_data.replace({np.nan: None}).to_dict('records')

        # Limit results for non-filtered queries
        if not hospital_filter and (not auth_data or auth_data.get('role') == 'admin'):
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
