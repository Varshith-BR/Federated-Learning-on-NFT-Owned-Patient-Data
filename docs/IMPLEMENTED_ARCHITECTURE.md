# Implemented System Architecture

## Overview

The NFT-based Federated Learning system for healthcare data management is implemented as a **three-layer architecture** that enables privacy-preserving collaborative machine learning across multiple healthcare institutions while maintaining patient consent control through blockchain-simulated NFT tokens.

---

## Architecture Layers

### 1. Presentation Layer (Web Interface)

**Technology**: Flask (Python) with Jinja2 templates, Bootstrap 5, Chart.js

**Implemented Portals**:

#### 1.1 Patient Portal (`/patient`)
- View personal medical records
- Manage NFT-based consent status (allow/deny training)
- Set consent expiry dates
- View consent history and blockchain transactions
- **Access Control**: Patient-specific data only (filtered by patient_id)

#### 1.2 Hospital Portal (`/hospital`)
- View institution-specific patient demographics
- Monitor data distribution and consent statistics
- Track patients by consent status
- View hospital-specific filtered datasets
- **Access Control**: Hospital-specific data only (filtered by hospital_id)

#### 1.3 Admin/Training Dashboard (`/training`)
- Configure FL training parameters (model type, rounds, privacy mode)
- Start and monitor federated learning training
- View real-time training metrics (accuracy, loss, convergence)
- Access global model state and training history
- **Access Control**: Admin-only access

#### 1.4 Blockchain Explorer (`/blockchain`)
- View immutable transaction ledger
- Track consent minting and updates
- Visualize blockchain blocks and transactions
- Audit trail for compliance

**Authentication System**:
- MetaMask wallet integration with Ethereum address verification
- Ganache local blockchain for deterministic address generation
- Role-based access control (Admin, Hospital, Patient)
- Session management with address validation
- Auto-logout on MetaMask account change

---

### 2. Application Layer (Backend Logic)

**Technology**: Flask REST API, Python 3.8+

#### 2.1 Core Components

**Flask Application (`app.py`)**:
- REST API endpoints for all portal functionalities
- Session-based authentication with role verification
- Data filtering based on authenticated user role
- Real-time training status tracking
- CSV-based data storage and retrieval

**API Endpoints**:
```
Authentication:
  POST /api/auth/verify        - Verify Ethereum address
  POST /api/auth/check         - Validate session
  GET  /logout                 - Clear session

Data Access (Role-Filtered):
  GET  /api/patients           - Get patient data
  GET  /api/nodes              - Get hospital statistics
  GET  /api/blockchain         - Get blockchain transactions
  GET  /api/consent_analytics  - Get consent statistics

Federated Learning (Admin Only):
  POST /api/start_training     - Start FL training
  GET  /api/training_status    - Get training progress
  GET  /api/training_history   - Get training history
  GET  /api/global_model       - Get global model state

Consent Management:
  POST /api/update_consent     - Update patient consent
```

#### 2.2 Federated Learning Engine (`federated_learning_engine.py`)

**Implemented Classes**:

**FederatedModel**:
- Supports 3 model types: Logistic Regression, Neural Network (MLP), SVM
- Scikit-learn based implementation
- Parameter extraction and aggregation
- Model serialization and loading

**FederatedLearningNode**:
- Represents individual hospital nodes
- Local data loading from CSV files
- Consent filtering: `D_filtered = {xi ∈ D : xi.allow_training = true}`
- Local model training on consented data
- Model parameter sharing

**FederatedLearningServer**:
- Node registration and coordination
- Global model initialization
- Federated averaging (FedAvg) algorithm
- Training round orchestration
- Performance metrics tracking

**Training Modes**:
1. **Standard Federated Learning**: Basic FedAvg aggregation
2. **Secure Aggregation**: Simulated MPC with masked updates
3. **Differential Privacy**: Gradient clipping and noise injection

**Supported Models**:
- **Logistic Regression**: L-BFGS solver, 1000 max iterations
- **Neural Network (MLP)**: 2 hidden layers (100, 50 units), ReLU activation, Adam optimizer
- **Support Vector Machine**: RBF kernel, probability estimates enabled

#### 2.3 Blockchain & NFT System (`blockchain_nft_system.py`)

**Implemented Classes**:

**Block**:
- SHA-256 based hashing
- Proof-of-work mining (configurable difficulty)
- Transaction storage
- Block validation

**PatientNFT**:
- Unique token ID generation
- Consent metadata storage (allow_training, expiry_date)
- Consent validation logic
- Patient-to-NFT mapping

**SmartContract**:
- NFT minting and registry
- Consent update functionality
- Consent verification for training
- Consent statistics aggregation

**BlockchainNetwork**:
- Genesis block creation
- Transaction pool management
- Block mining and chain validation
- Smart contract deployment
- Immutable audit trail

**NFTConsentManager**:
- High-level consent management API
- Patient consent updates
- Bulk consent verification
- Consent analytics and reporting

---

### 3. Data Layer

**Technology**: CSV files (simulating distributed databases)

#### 3.1 Data Files

**Patient Dataset (`patient_dataset.csv`)**:
- Comprehensive patient medical records
- Demographics, conditions, medications, lab results
- 1000+ patient records across 8 hospitals

**NFT Metadata (`nft_metadata.csv`)**:
- NFT token mappings
- Consent status (allow_training)
- Expiry dates
- Patient-to-token relationships

**Hospital Node Data (`node_*.csv`)**:
- Hospital-specific filtered datasets
- 8 hospitals implemented:
  - St. Mary's Hospital
  - City Medical Center
  - University Medical Center
  - Regional Healthcare
  - Metro General Hospital
  - Children's Medical Center
  - Community Health Network
  - Veterans Affairs Hospital

**Address Mapping (`address_mapping.csv`)**:
- Ethereum address to role mapping
- 30 deterministic Ganache accounts:
  - Accounts 0-1: Admins
  - Accounts 2-9: Hospitals
  - Accounts 10-29: Patients

#### 3.2 Data Flow

```
1. Patient → Update Consent → NFT Metadata CSV → Blockchain Transaction
2. Admin → Start Training → FL Engine → Load Consented Data
3. FL Engine → Apply Consent Filter → Local Training per Node
4. Nodes → Send Model Updates → Server Aggregation (FedAvg)
5. Server → Update Global Model → Store Training History
6. Dashboard → Real-time Metrics → User Interface
```

---

## Smart Contract (Solidity)

**File**: `contracts/PatientConsent.sol`

**Implementation**: ERC-721 based NFT contract

**Key Features**:
- Minting consent NFTs for patients
- Consent metadata structure (patientId, dataHash, allowTraining, expiryDate)
- Owner-only consent updates
- Consent validation function (`isConsentValid`)
- Event emission for consent changes
- IPFS hash storage for detailed consent documents

**Note**: Solidity contract provided for future blockchain deployment; current system uses Python simulation.

---

## Security Features

### Authentication & Authorization
- Ethereum address-based authentication via MetaMask
- Role-based access control (RBAC)
- Session validation on every request
- Automatic logout on account change
- Protected routes with `@require_auth` decorator

### Data Privacy
- No centralized patient data storage
- Data remains on local hospital servers (CSV files)
- Only model parameters shared, never raw data
- Consent filtering before every training round
- Differential privacy option with noise injection

### Blockchain Security
- SHA-256 cryptographic hashing
- Proof-of-work mining
- Immutable transaction ledger
- Chain validation
- Tamper-proof audit trail

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.8+, Flask |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **ML Libraries** | Scikit-learn, NumPy, Pandas |
| **Charts** | Chart.js |
| **Blockchain** | Python simulation (SHA-256) |
| **Smart Contract** | Solidity (ERC-721) |
| **Authentication** | MetaMask, Ganache, ethers.js |
| **Data Storage** | CSV files |
| **Session Management** | Flask sessions |

---

## Key Algorithms

### Federated Averaging (FedAvg)

**Standard FL Objective**:
```
min_w Σ(k=1 to K) (n_k/n) * F_k(w)
```

**Consent-Filtered FL**:
```
D_k^(t) = {(x_i, y_i) ∈ D_k | Verify(NFT_i, B_t) == True}
```

Where:
- `D_k^(t)`: Filtered dataset at hospital k for round t
- `Verify()`: NFT consent validation function
- `B_t`: Blockchain state at round t

### Consent Filtering
```python
D_filtered = {x_i ∈ D : x_i.allow_training = true AND 
                         (x_i.expiry_date is None OR 
                          x_i.expiry_date > current_time)}
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                 │
│  (Browser + MetaMask)                                   │
│  - Patient Portal  - Hospital Portal  - Admin Portal    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS/WebSocket
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Flask Application                       │
│  - REST API  - Authentication  - Session Management     │
└────────┬───────────────────────────────────────┬────────┘
         │                                       │
         │                                       │
┌────────▼────────────┐              ┌──────────▼─────────┐
│  FL Engine          │              │  Blockchain System │
│  - FedAvg           │              │  - NFT Manager     │
│  - Model Training   │◄────────────►│  - Smart Contract  │
│  - Aggregation      │   Consent    │  - Audit Trail     │
└────────┬────────────┘   Validation └────────────────────┘
         │
         │
┌────────▼────────────────────────────────────────────────┐
│                    Data Layer (CSV)                      │
│  - patient_dataset.csv  - nft_metadata.csv              │
│  - node_*.csv (8 hospitals)  - address_mapping.csv      │
└─────────────────────────────────────────────────────────┘
```

---

## Implemented Features Summary

✅ **Privacy-Preserving FL**: Data never leaves hospital nodes  
✅ **NFT-Based Consent**: Blockchain-simulated consent tokens  
✅ **Dynamic Consent**: Real-time consent updates affect training  
✅ **Multi-Model Support**: 3 ML algorithms (LR, NN, SVM)  
✅ **3 Training Modes**: Standard, Secure Aggregation, Differential Privacy  
✅ **Role-Based Access**: Admin, Hospital, Patient portals  
✅ **MetaMask Authentication**: Ethereum address-based login  
✅ **Blockchain Explorer**: Immutable audit trail visualization  
✅ **Real-Time Monitoring**: Live training metrics and progress  
✅ **Consent Analytics**: Statistics and trends dashboard  
✅ **8 Hospital Nodes**: Simulated multi-institutional network  
✅ **1000+ Patient Records**: Synthetic healthcare dataset  

---

## System Limitations

⚠️ **Simulation-Based**: Blockchain is Python-simulated, not deployed on actual Ethereum  
⚠️ **CSV Storage**: Uses CSV files instead of production databases  
⚠️ **Local Deployment**: Designed for localhost, not production-ready  
⚠️ **Synthetic Data**: Uses generated patient data, not real medical records  
⚠️ **No IPFS**: IPFS integration mentioned but not implemented  
⚠️ **Basic Security**: Development-level security, not production-hardened  

---

**Document Version**: 1.0  
**Last Updated**: December 9, 2025  
**Based on**: Actual implementation analysis
