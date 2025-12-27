
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
import logging
from concurrent.futures import ThreadPoolExecutor
import threading
import time


class FederatedModel:
    """Base class for federated learning models"""

    def __init__(self, model_type: str = 'random_forest'):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_fitted = False

        # Initialize model based on type
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the appropriate model"""
        if self.model_type == 'random_forest':
            # Random Forest (Ensemble) - 100 Trees
            self.model = RandomForestClassifier(n_estimators=100, criterion='gini')
        elif self.model_type == 'mlp':
            # Neural Network (Deep MLP) - 128-64-32
            self.model = MLPClassifier(hidden_layer_sizes=(128, 64, 32), activation='relu', solver='adam', max_iter=500)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def preprocess_data(self, data: pd.DataFrame, target_column: str = 'primary_condition') -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess data for training"""
        # Select relevant features
        feature_columns = [
            'age', 'systolic_bp', 'diastolic_bp', 'heart_rate', 
            'temperature', 'glucose_level', 'cholesterol', 'bmi'
        ]

        # Handle missing features
        available_features = [col for col in feature_columns if col in data.columns]

        X = data[available_features].fillna(data[available_features].mean())
        y = data[target_column].fillna('Unknown')

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)

        return X_scaled, y_encoded

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train the model"""
        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")

        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            # For SVM without probability=True
            return np.eye(len(self.label_encoder.classes_))[self.predict(X)]

    def get_parameters(self) -> dict:
        """Get model parameters for federated averaging"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before extracting parameters")

        if self.model_type == 'random_forest':
            return {
                'estimators_': self.model.estimators_,
                'n_classes_': self.model.n_classes_,
                'classes_': self.model.classes_
            }
        elif self.model_type == 'mlp':
            return {
                'coefs_': [coef.copy() for coef in self.model.coefs_],
                'intercepts_': [intercept.copy() for intercept in self.model.intercepts_],
                'classes_': self.model.classes_.copy()
            }
        else:
            # For SVM, we'll return support vectors and other parameters
            return {
                'support_vectors_': self.model.support_vectors_.copy() if hasattr(self.model, 'support_vectors_') else None,
                'support_': self.model.support_.copy() if hasattr(self.model, 'support_') else None,
                'n_support_': self.model.n_support_.copy() if hasattr(self.model, 'n_support_') else None,
                'classes_': self.model.classes_.copy()
            }

    def set_parameters(self, parameters: dict):
        """Set model parameters from federated averaging"""
        if self.model_type == 'random_forest':
             # In a real FL Random Forest, we aggregate trees from all nodes
             # parameters['estimators_'] is a list of trees from all nodes
             if 'estimators_' in parameters:
                 self.model.estimators_ = parameters['estimators_']
                 self.model.n_estimators = len(self.model.estimators_)
             if 'classes_' in parameters:
                 self.model.classes_ = parameters['classes_']
                 self.model.n_classes_ = len(self.model.classes_)

        elif self.model_type == 'mlp':
            # Set coefficients and intercepts
            if 'coefs_' in parameters and 'intercepts_' in parameters:
                self.model.coefs_ = parameters['coefs_']
                self.model.intercepts_ = parameters['intercepts_']
                
            if 'classes_' in parameters:
                self.model.classes_ = parameters['classes_']
                # Force re-initialization of properties if needed
                self.model.n_outputs_ = len(self.model.classes_)
                self.model.out_activation_ = 'logistic' if self.model.n_outputs_ == 1 else 'softmax'
        
        # SVM parameter setting is more complex and model-dependent
        
        self.is_fitted = True

    def save(self, filepath: str):
        """Save model to file"""
        model_data = {
            'model_type': self.model_type,
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'is_fitted': self.is_fitted
        }
        joblib.dump(model_data, filepath)

    @classmethod
    def load(cls, filepath: str):
        """Load model from file"""
        model_data = joblib.load(filepath)
        instance = cls(model_data['model_type'])
        instance.model = model_data['model']
        instance.scaler = model_data['scaler']
        instance.label_encoder = model_data['label_encoder']
        instance.is_fitted = model_data['is_fitted']
        return instance


class FederatedLearningNode:
    """Individual node in the federated learning network"""

    def __init__(self, node_id: str, hospital_name: str, data_path: str):
        self.node_id = node_id
        self.hospital_name = hospital_name
        self.data_path = data_path
        self.data = None
        self.model = None
        self.training_history = []
        self.last_update = None

        # Load data
        self.load_data()

        # Setup logging
        self.logger = logging.getLogger(f"FL_Node_{node_id}")
        self.logger.setLevel(logging.INFO)

    def load_data(self):
        """Load and preprocess node data"""
        try:
            self.data = pd.read_csv(self.data_path)
            self.logger.info(f"Loaded {len(self.data)} records for {self.hospital_name}")
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            self.data = pd.DataFrame()  # Empty dataframe

    def apply_consent_filter(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply consent filtering as per Equation 3.1: D_filtered = {xi ∈ D : xi.allow_training = true}"""
        if 'allow_training' not in data.columns:
            self.logger.warning("No consent column found, using all data")
            return data

        # Filter for consented data
        consented_data = data[data['allow_training'] == True].copy()

        # Check for expired consent
        if 'expiry_date' in consented_data.columns:
            current_date = datetime.now()
            unexpired_mask = (consented_data['expiry_date'].isna()) | (pd.to_datetime(consented_data['expiry_date'], errors='coerce') > current_date)
            consented_data = consented_data[unexpired_mask]

        self.logger.info(f"Consent filtering: {len(data)} -> {len(consented_data)} records")
        return consented_data

    def local_train(self, model_type: str = 'random_forest', epochs: int = 1) -> dict:
        """Perform local training on consented data"""
        if self.data is None or len(self.data) == 0:
            return {
                'success': False,
                'message': 'No data available',
                'metrics': {}
            }

        # Apply consent filter
        training_data = self.apply_consent_filter(self.data)

        if len(training_data) == 0:
            return {
                'success': False,
                'message': 'No consented data available',
                'metrics': {}
            }

        try:
            # Initialize model if not exists
            if self.model is None or self.model.model_type != model_type:
                self.model = FederatedModel(model_type)

            # Preprocess data
            X, y = self.model.preprocess_data(training_data)

            # Split for validation - randomness enabled
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, stratify=y
            )

            # Train model
            self.model.fit(X_train, y_train)

            # Evaluate
            train_predictions = self.model.predict(X_train)
            val_predictions = self.model.predict(X_val)

            train_accuracy = accuracy_score(y_train, train_predictions)
            val_accuracy = accuracy_score(y_val, val_predictions)

            # Calculate loss (simplified)
            train_loss = 1.0 - train_accuracy
            val_loss = 1.0 - val_accuracy

            metrics = {
                'train_accuracy': train_accuracy,
                'val_accuracy': val_accuracy,
                'train_loss': train_loss,
                'val_loss': val_loss,
                'data_points': len(training_data),
                'consented_data_points': len(training_data)
            }

            # Store training history
            self.training_history.append({
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics,
                'model_type': model_type,
                'epochs': epochs
            })

            self.last_update = datetime.now()

            return {
                'success': True,
                'message': 'Local training completed',
                'metrics': metrics,
                'parameters': self.model.get_parameters() if self.model.is_fitted else {}
            }

        except Exception as e:
            self.logger.error(f"Error in local training: {e}")
            return {
                'success': False,
                'message': f'Training error: {str(e)}',
                'metrics': {}
            }

    def update_model(self, global_parameters: dict):
        """Update local model with global parameters"""
        try:
            if self.model is None:
                self.logger.warning("No local model to update")
                return False

            self.model.set_parameters(global_parameters)
            self.last_update = datetime.now()
            return True

        except Exception as e:
            self.logger.error(f"Error updating model: {e}")
            return False

    def get_node_info(self) -> dict:
        """Get comprehensive node information"""
        consented_data = self.apply_consent_filter(self.data) if self.data is not None else pd.DataFrame()

        return {
            'node_id': self.node_id,
            'hospital_name': self.hospital_name,
            'total_data_points': len(self.data) if self.data is not None else 0,
            'consented_data_points': len(consented_data),
            'consent_rate': len(consented_data) / len(self.data) if self.data is not None and len(self.data) > 0 else 0,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'training_rounds': len(self.training_history),
            'model_type': self.model.model_type if self.model else None,
            'is_fitted': self.model.is_fitted if self.model else False
        }


class FederatedLearningServer:
    """Central server for federated learning coordination"""

    def __init__(self):
        self.nodes: Dict[str, FederatedLearningNode] = {}
        self.global_model = None
        self.training_rounds = []
        self.current_round = 0
        self.is_training = False

        # Setup logging
        self.logger = logging.getLogger("FL_Server")
        self.logger.setLevel(logging.INFO)

    def register_node(self, node_id: str, hospital_name: str, data_path: str) -> bool:
        """Register a new node"""
        try:
            node = FederatedLearningNode(node_id, hospital_name, data_path)
            self.nodes[node_id] = node
            self.logger.info(f"Registered node {node_id}: {hospital_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error registering node {node_id}: {e}")
            return False

    def initialize_global_model(self, model_type: str = 'random_forest'):
        """Initialize the global model"""
        self.global_model = FederatedModel(model_type)
        self.logger.info(f"Initialized global {model_type} model")

    def federated_averaging(self, local_parameters: List[dict], weights: List[float]) -> dict:
        """Perform federated averaging of local model parameters"""
        if not local_parameters or not weights:
            raise ValueError("No parameters or weights provided for averaging")

        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # Average parameters based on model type
        if self.global_model.model_type == 'random_forest':
            # Federated Forest: Aggregate all trees from all local models
            aggregated_estimators = []
            for params in local_parameters:
                if 'estimators_' in params:
                    aggregated_estimators.extend(params['estimators_'])
            
            # Return the full ensemble of trees
            # This mathematically represents "averaging" predictions across all local knowledge
            return {
                'estimators_': aggregated_estimators,
                'classes_': local_parameters[0]['classes_']
            }

        elif self.global_model.model_type == 'mlp':
            # Standard FedAvg: Weighted average of weights and biases
            avg_coefs = []
            avg_intercepts = []

            # Initialize with zeros based on the first model's architecture
            first_params = local_parameters[0]
            for layer_idx in range(len(first_params['coefs_'])):
                avg_coefs.append(np.zeros_like(first_params['coefs_'][layer_idx]))
                avg_intercepts.append(np.zeros_like(first_params['intercepts_'][layer_idx]))

            # Weighted sum
            total_weight = sum(weights)
            normalized_weights = [w / total_weight for w in weights]

            for params, weight in zip(local_parameters, normalized_weights):
                for layer_idx in range(len(params['coefs_'])):
                    avg_coefs[layer_idx] += weight * params['coefs_'][layer_idx]
                    avg_intercepts[layer_idx] += weight * params['intercepts_'][layer_idx]

            return {
                'coefs_': avg_coefs,
                'intercepts_': avg_intercepts,
                'classes_': first_params['classes_']
            }
        
        else:
             raise ValueError(f"Unsupported model type for aggregation: {self.global_model.model_type}")

    def training_round(self, model_type: str = 'random_forest', min_participants: int = 1) -> dict:
        """Execute one round of federated training"""
        if len(self.nodes) == 0:
            return {
                'success': False,
                'message': 'No nodes registered'
            }

        self.current_round += 1
        round_start_time = datetime.now()

        self.logger.info(f"Starting training round {self.current_round}")

        # Initialize global model if needed
        if self.global_model is None:
            self.initialize_global_model(model_type)

        # Collect local training results
        local_results = {}
        local_parameters = []
        weights = []

        # Train on each node
        for node_id, node in self.nodes.items():
            self.logger.info(f"Training on node {node_id}")
            result = node.local_train(model_type)

            if result['success'] and result['parameters']:
                local_results[node_id] = result
                local_parameters.append(result['parameters'])
                weights.append(result['metrics']['consented_data_points'])
            else:
                self.logger.warning(f"Node {node_id} failed training: {result['message']}")

        # Check minimum participation
        if len(local_parameters) < min_participants:
            return {
                'success': False,
                'message': f'Insufficient participants: {len(local_parameters)} < {min_participants}'
            }

        # Perform federated averaging
        try:
            global_parameters = self.federated_averaging(local_parameters, weights)

            # Update global model
            self.global_model.set_parameters(global_parameters)

            # Update all nodes with global parameters
            for node_id, node in self.nodes.items():
                node.update_model(global_parameters)

            # Calculate global metrics
            total_data_points = sum(result['metrics']['consented_data_points'] 
                                  for result in local_results.values())

            weighted_accuracy = sum(
                result['metrics']['val_accuracy'] * result['metrics']['consented_data_points']
                for result in local_results.values()
            ) / total_data_points if total_data_points > 0 else 0

            weighted_loss = sum(
                result['metrics']['val_loss'] * result['metrics']['consented_data_points']
                for result in local_results.values()
            ) / total_data_points if total_data_points > 0 else 0

            # Store round results
            round_result = {
                'round': self.current_round,
                'timestamp': round_start_time.isoformat(),
                'participating_nodes': len(local_parameters),
                'total_nodes': len(self.nodes),
                'total_consented_data': total_data_points,
                'global_accuracy': weighted_accuracy,
                'global_loss': weighted_loss,
                'local_results': local_results,
                'duration': (datetime.now() - round_start_time).total_seconds()
            }

            self.training_rounds.append(round_result)

            self.logger.info(f"Round {self.current_round} completed - Accuracy: {weighted_accuracy:.4f}, Loss: {weighted_loss:.4f}")

            return {
                'success': True,
                'round_result': round_result
            }

        except Exception as e:
            self.logger.error(f"Error in federated averaging: {e}")
            return {
                'success': False,
                'message': f'Federated averaging failed: {str(e)}'
            }

    def train(self, num_rounds: int, model_type: str = 'random_forest', min_participants: int = 1) -> List[dict]:
        """Run multiple rounds of federated training"""
        self.is_training = True
        results = []

        self.logger.info(f"Starting federated training: {num_rounds} rounds, {model_type} model")

        for round_num in range(num_rounds):
            result = self.training_round(model_type, min_participants)
            results.append(result)

            if not result['success']:
                self.logger.error(f"Training stopped at round {round_num + 1}: {result['message']}")
                break

        self.is_training = False
        self.logger.info("Federated training completed")

        return results

    def evaluate_global_model(self, test_data_path: Optional[str] = None) -> dict:
        """Evaluate the global model"""
        if self.global_model is None or not self.global_model.is_fitted:
            return {
                'success': False,
                'message': 'No trained global model available'
            }

        # If no test data provided, use validation data from nodes
        if test_data_path is None:
            # Collect validation metrics from all nodes
            total_accuracy = 0
            total_samples = 0

            for node in self.nodes.values():
                if node.training_history:
                    last_training = node.training_history[-1]
                    metrics = last_training['metrics']
                    samples = metrics['consented_data_points']

                    total_accuracy += metrics['val_accuracy'] * samples
                    total_samples += samples

            global_accuracy = total_accuracy / total_samples if total_samples > 0 else 0

            return {
                'success': True,
                'global_accuracy': global_accuracy,
                'total_samples': total_samples,
                'message': 'Evaluation based on node validation data'
            }

        else:
            # Evaluate on external test data
            try:
                test_data = pd.read_csv(test_data_path)

                # Apply consent filter
                consented_test_data = test_data[test_data.get('allow_training', True) == True]

                if len(consented_test_data) == 0:
                    return {
                        'success': False,
                        'message': 'No consented test data available'
                    }

                # Preprocess and evaluate
                X_test, y_test = self.global_model.preprocess_data(consented_test_data)
                predictions = self.global_model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)

                return {
                    'success': True,
                    'test_accuracy': accuracy,
                    'test_samples': len(consented_test_data),
                    'classification_report': classification_report(y_test, predictions, output_dict=True),
                    'message': 'Evaluation on external test data'
                }

            except Exception as e:
                return {
                    'success': False,
                    'message': f'Error evaluating on test data: {str(e)}'
                }

    def get_training_summary(self) -> dict:
        """Get comprehensive training summary"""
        if not self.training_rounds:
            return {
                'total_rounds': 0,
                'message': 'No training completed'
            }

        latest_round = self.training_rounds[-1]

        return {
            'total_rounds': len(self.training_rounds),
            'current_round': self.current_round,
            'final_accuracy': latest_round['global_accuracy'],
            'final_loss': latest_round['global_loss'],
            'total_nodes': len(self.nodes),
            'participating_nodes': latest_round['participating_nodes'],
            'total_consented_data': latest_round['total_consented_data'],
            'training_history': self.training_rounds,
            'model_type': self.global_model.model_type if self.global_model else None,
            'is_training': self.is_training
        }

    def save_global_model(self, filepath: str) -> bool:
        """Save the global model"""
        try:
            if self.global_model is None:
                return False

            self.global_model.save(filepath)
            self.logger.info(f"Global model saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            return False

    def load_global_model(self, filepath: str) -> bool:
        """Load a global model"""
        try:
            self.global_model = FederatedModel.load(filepath)
            self.logger.info(f"Global model loaded from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            return False


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Initialize federated learning server
    fl_server = FederatedLearningServer()

    # Register nodes (hospital datasets)
    hospital_files = [
        ('node_metro_general', 'Metro General Hospital', 'node_metro_general_hospit_data.csv'),
        ('node_regional', 'Regional Healthcare System', 'node_regional_healthcare__data.csv'),
        ('node_st_marys', 'St. Mary Hospital', 'node_st._marys_hospital_data.csv'),
        ('node_university', 'University Medical Center', 'node_university_medical_c_data.csv')
    ]

    registered_count = 0
    for node_id, hospital_name, file_path in hospital_files:
        if os.path.exists(file_path):
            if fl_server.register_node(node_id, hospital_name, file_path):
                registered_count += 1

    print(f"Registered {registered_count} nodes")

    if registered_count > 0:
        # Run federated training
        print("Starting federated training...")
        training_results = fl_server.train(num_rounds=3, model_type='random_forest', min_participants=1)

        # Print results
        for i, result in enumerate(training_results):
            if result['success']:
                round_result = result['round_result']
                print(f"Round {i+1}: Accuracy={round_result['global_accuracy']:.4f}, "
                      f"Loss={round_result['global_loss']:.4f}, "
                      f"Participants={round_result['participating_nodes']}")

        # Get training summary
        summary = fl_server.get_training_summary()
        print(f"\nTraining Summary:")
        print(f"Final Accuracy: {summary['final_accuracy']:.4f}")
        print(f"Total Consented Data: {summary['total_consented_data']}")

        # Save model
        fl_server.save_global_model('global_fl_model.joblib')
    else:
        print("No nodes registered. Please ensure hospital data files exist.")
