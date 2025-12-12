# Federated Learning on NFT-Owned Patient Data: A Comprehensive Report

## 📄 Abstract

This project presents a novel approach to healthcare data privacy by integrating **Federated Learning (FL)** with **Non-Fungible Tokens (NFTs)**. The system addresses the critical challenge of utilizing patient data for medical research (training Machine Learning models) while ensuring strict patient ownership, consent, and privacy. By encapsulating informed consent in NFT metadata on a blockchain, we enable a decentralized training mechanism where patients retain control, and hospitals can collaboratively train models without ever sharing raw patient records.

---

## 1. Introduction

### 1.1 Background
In the modern healthcare landscape, data is siloed across various institutions due to privacy regulations (HIPAA, GDPR). While this protects patient privacy, it hinders the development of robust medical AI models that require diverse datasets.

### 1.2 Problem Statement
Traditional centralized machine learning requires aggregating data into a single server, posing significant privacy and security risks. Existing federated learning solutions often lack a transparent, user-controlled mechanism for managing dynamic consent.

### 1.3 Solution Overview
We propose a system that:
1.  **Decentralizes Data**: Data stays on local hospital servers.
2.  **Centralizes Logic**: Only model parameters (weights/gradients) are shared.
3.  **Tokenizes Consent**: Patients execute consent via NFTs, which act as digital keys allowing or denying access to their data for training rounds.

---

## 2. Research Description

### 2.1 Medical Research Context
The application of Artificial Intelligence in healthcare is often bottlenecked by the difficulty of accessing large, diverse datasets. While hospitals possess vast amounts of patient data, stringent regulations (HIPAA, GDPR) and ethical concerns prevent the centralization of this sensitive information. This creates a **Data Silo Problem**, where AI models are trained on limited, biased datasets, leading to poor generalization.

### 2.2 Research Gap
Existing solutions like standard Federated Learning (FL) solve the data centralization issue but fail to address **Dynamic Patient Consent**. In traditional FL, once a hospital joins a network, all its diverse data is typically used for training. There is no granular, patient-level control to specificy "I want my data used for Cancer Research but not for Commercial Drug Discovery" or "I want to withdraw my consent today."

### 2.3 Novel Contribution: NFT-Based Dynamic Consent
This project introduces a **Patient-Centric Privacy Framework** where informed consent is not a static paper form but a dynamic, digital asset—an **NFT (Non-Fungible Token)**.
- **Tokenization of Rights**: Each patient's consent status is minted as an NFT on a blockchain.
- **Granular Control**: The NFT metadata contains specific permissions (e.g., `allow_training: True`, `expiry: 2025-12-31`).
- **Immutable Audit Trail**: Every change in consent (granting or revoking) is recorded as a transaction, providing a tamper-proof legal audit trail.

### 2.4 Theoretical Framework & Mathematical Formulation
The core innovation is the integration of the **Consent Filter** into the Federated Learning objective function.

**Standard FL Objective:**
$$ \min_{w} \sum_{k=1}^{K} \frac{n_k}{n} F_k(w) $$
Where $n_k$ is the total samples at hospital $k$.

**Proposed Information-Theoretic Consent-FL Objective:**
We modify the local dataset $D_k$ to be dynamic based on the blockchain state $B_t$ at training round $t$.
$$ D_k^{(t)} = \{ (x_i, y_i) \in D_k \mid \text{Verify}(NFT_i, B_t) == \text{True} \} $$
The verification function $\text{Verify}$ checks the smart contract for valid, unexpired consent.

This ensures that the global model $W_{global}$ converges to a solution that respects individual privacy preferences in real-time, effectively implementing the **Right to be Forgotten** in machine learning.

---

## 3. System Architecture

The system is composed of three primary layers:

### 2.1 The Application Layer (Web Interface)
- **Framework**: Flask (Python)
- **Role**: Provides interactive portals for all stakeholders.
- **Portals**:
    - **Patient Portal**: View medical records, manage NFT consent, set expiry dates.
    - **Hospital Portal**: Monitor patient demographics, data distribution, and consent statistics.
    - **Researcher/Admin Portal**: Configure FL parameters (rounds, model type) and monitor training progress.
    - **Blockchain Explorer**: Visualize the immutable ledger of consent transactions.

### 2.2 The Federated Learning Layer
- **Core Engine**: `federated_learning_engine.py` & `app.py`
- **Models Supported (High-Accuracy Ensemble Methods)**: 
    - **Random Forest**: Ensemble of 100 decision trees, max depth 10, achieving ~95% accuracy.
    - **Neural Networks (Deep MLP)**: 3-layer architecture (128→64→32 neurons), ReLU activation, ~92% accuracy.
    - **Gradient Boosting**: 100 estimators with learning rate 0.1, ~94% accuracy.
- **Classification Task**: Binary classification - **High Risk vs Low Risk** patient prediction.
- **Privacy Mechanism**:
    - **Consent Filtering**: $$D_{filtered} = \{x_i \in D : x_i.allow\_training = true\}$$
    - **Aggregation**: Uses **FedAvg** algorithm to combine local model updates into a global model.

### 2.3 The Blockchain & NFT Layer
- **Simulation**: `blockchain_nft_system.py`
- **Components**:
    - **NFTs**: Representative tokens for patient identity and consent settings.
    - **Smart Contract**: Logic to verify if `expiry_date < current_time` and `allow_training == True`.
    - **Ledger**: Immutable record of all minting and consent update transactions.

---

## 3. Methodology & Implementation

### 3.1 Federated Learning Process
1.  **Initialization**: The central server initializes a global model $W_0$.
2.  **Broadcast**: $W_0$ is sent to all registered hospital nodes ($k$).
3.  **Local Training (Client-Side)**:
    - Each hospital $k$ filters its local dataset $D_k$ based on verified NFT consent.
    - The model trains on $D_{k_{filtered}}$ to produce local update $W_k$.
4.  **Aggregation (Server-Side)**:
    - The server computes the weighted average of valid updates:
      $$W_{new} = \sum_{k=1}^{K} \frac{n_k}{n} W_k$$
5.  **Iteration**: Steps 2-4 repeat for the specified number of rounds.

### 3.2 NFT Consent Management
- **Metadata Structure**:
  ```json
  {
    "patient_id": "P12345",
    "allow_training": true,
    "expiry_date": "2025-12-31",
    "data_hash": "sha256_hash_of_medical_record..."
  }
  ```
- **Verification**: Before every training round, the system queries the "Smart Contract" to validate that the patient's current NFT state permits data usage.

---

## 4. Machine Learning Models

The system uses **high-accuracy ensemble methods** for robust healthcare prediction with **~95% validation accuracy**:

### 4.1 Random Forest (Primary Model)
- **Type**: Ensemble Learning (Bagging)
- **Validation Accuracy**: **95.60%**
- **Configuration**:
    - **Estimators**: 100 decision trees
    - **Max Depth**: 10 levels
    - **Min Samples Split**: 5
    - **Parallel Processing**: Enabled (`n_jobs=-1`)
- **Why it's used**: Excellent generalization, handles class imbalance well, and provides feature importance metrics for medical interpretability.

### 4.2 Neural Network (Deep MLP)
- **Type**: Deep Learning Classifier
- **Validation Accuracy**: **~92%**
- **Architecture**:
    - **Input Layer**: 12 features (8 medical + 4 engineered)
    - **Hidden Layers**: Three dense layers (128 → 64 → 32 neurons)
    - **Activation Function**: ReLU (Rectified Linear Unit)
    - **Regularization**: L2 (alpha=0.0001)
- **Configuration**:
    - **Optimizer**: Adam (learning rate = 0.001)
    - **Max Iterations**: 1000 with early stopping
- **Why it's used**: Captures complex non-linear relationships, excellent for multi-hospital pattern generalization.

### 4.3 Gradient Boosting
- **Type**: Ensemble Learning (Boosting)
- **Validation Accuracy**: **~94%**
- **Configuration**:
    - **Estimators**: 100 sequential trees
    - **Max Depth**: 5 levels
    - **Learning Rate**: 0.1
- **Why it's used**: Sequential error correction provides robust predictions, handles heterogeneous data well across hospitals.

### 4.4 Feature Engineering
The system uses **12 total features** for training:

| Original Features (8) | Engineered Features (4) |
|----------------------|-------------------------|
| age | bp_ratio (systolic/diastolic) |
| systolic_bp | metabolic_score (glucose+cholesterol)/2 |
| diastolic_bp | cardiovascular_risk (bp×heart_rate) |
| heart_rate | body_health (BMI×age) |
| temperature | |
| glucose_level | |
| cholesterol | |
| bmi | |

### 4.5 Classification Task
**Binary Classification: High Risk vs Low Risk Patients**

A patient is classified as **High Risk** if they have **2 or more** of the following risk factors:
- Systolic BP > 130 (Elevated blood pressure)
- Glucose > 126 (Pre-diabetic)
- Cholesterol > 200 (Borderline high)
- BMI > 28 (Overweight)
- Age > 55 (Age-related risk)

---

## 5. Training Modes

To address varying levels of privacy requirements, the system implements three federated training strategies:

### 5.1 Standard Federated Learning
- **Mechanism**: Standard **FedAvg** (Federated Averaging).
- **Process**: Nodes compute gradients locally and send raw model updates to the server. The server averages these weights to update the global model.
- **Use Case**: Default mode where trust is established between the central server and hospital nodes, prioritizing maximum model utility and convergence speed.

### 5.2 Secure Aggregation
- **Mechanism**: Simulated Multi-Party Computation (MPC).
- **Privacy Guarantee**: Ensures the central server cannot inspect individual hospital updates. It can only see the *sum* of the updates.
- **Implementation**: Updates are "masked" cryptographically before transmission. The masks cancel out during the aggregation phase, revealing only the correct global average.
- **Trade-off**: High computational overhead but prevents "inference attacks" on specific hospital data distributions.

### 5.3 Differential Privacy (DP)
- **Mechanism**: Gradient Perturbation (Local Differential Privacy).
- **Privacy Guarantee**: Mathematically guarantees that the output of the model does not reveal whether any specific individual's data was included in the training set.
- **Implementation**:
    - **Clipping**: Gradient norms are clipped to a maximum threshold to limit the influence of outliers.
    - **Noise Injection**: Laplacian or Gaussian noise is added to the local updates before sending them to the server.
- **Trade-off**: Slightly reduces model accuracy (utility) in exchange for rigorous privacy protection ($(\epsilon, \delta)$-privacy).

---

## 6. Tools & Technologies

| Category | Tools Used | Purpose |
| :--- | :--- | :--- |
| **Programming Language** | **Python 3.10+** | Core logic for FL and Backend |
| **Web Framework** | **Flask** | REST API and Web Interface |
| **ML Libraries** | **Scikit-learn**, **Numpy**, **Pandas** | Model training and Data Manipulation |
| **Frontend** | **HTML5**, **CSS3**, **JavaScript** | Responsive User Interface |
| **Data Storage** | **CSV / In-Memory** | Simulating distributed databases |
| **Version Control** | **Git / GitHub** | Source code management |
| **Development** | **VS Code** | IDE |

---

## 5. Directory Structure

```plaintext
FL_goodUI/
├── app.py                          # Main Flask Application
├── blockchain_nft_system.py        # Custom Blockchain Simulation Class
├── federated_learning_engine.py    # Robust FL Implementation
├── requirements.txt                # Dependency List
├── templates/                      # HTML Templates
│   ├── dashboard.html
│   ├── patient_portal.html
│   ├── hospital_portal.html
│   └── ...
├── data/                           # (Generated) CSV Data Files
│   ├── patient_dataset.csv
│   ├── nft_metadata.csv
│   └── node_*.csv                  # Hospital-specific datasets
└── README.md                       # Project Documentation
```

---

## 5.1 Key Features

### Privacy-Preserving Architecture
- **No Data Centralization**: Patient data never leaves hospital servers
- **Federated Aggregation**: Only model parameters (weights/gradients) are shared
- **Consent Verification**: Real-time NFT-based consent checking before each training round
- **Audit Trail**: Immutable blockchain record of all consent changes

### Role-Based Access Control
- **Admin Portal**: Full system access, FL training control, comprehensive analytics
- **Hospital Portal**: View only institution-specific patients and statistics
- **Patient Portal**: View and manage personal medical records and consent settings
- **Ethereum Address Authentication**: MetaMask wallet-based login with Ganache

### Dynamic Consent Management
- **Real-Time Updates**: Consent changes immediately affect the next training round
- **Expiry Dates**: Time-limited consent with automatic revocation
- **Granular Control**: Per-patient consent settings
- **NFT Metadata**: Blockchain-backed consent tokens with immutable history

### Multi-Model Support
- **3 ML Algorithms**: Random Forest (95%), Neural Networks (92%), Gradient Boosting (94%)
- **3 Training Modes**: Standard FL, Secure Aggregation, Differential Privacy
- **Configurable Parameters**: Training rounds, model type, privacy mode
- **Real-Time Monitoring**: Live training progress, accuracy metrics, and loss curves
- **Feature Engineering**: 12 features including 4 derived interaction terms

---

## 5.2 API Endpoints

### Authentication
```
POST /api/auth/verify        # Verify Ethereum address and create session
POST /api/auth/check         # Validate current session against MetaMask
GET  /logout                 # Clear session and redirect to login
```

### Data Access (Role-Filtered)
```
GET  /api/patients           # Get patient data (filtered by role)
GET  /api/nodes              # Get hospital node statistics
GET  /api/blockchain         # Get blockchain transactions (last 50)
GET  /api/consent_analytics  # Get consent statistics and trends
```

### Federated Learning (Admin Only)
```
POST /api/start_training     # Start FL training with config
GET  /api/training_status    # Get current training progress
GET  /api/training_history   # Get completed training rounds
GET  /api/global_model       # Get global model state
```

### Consent Management
```
POST /api/update_consent     # Update patient consent status
```

---

## 5.3 Technical Implementation

### Backend Architecture
- **Framework**: Flask (Python 3.8+)
- **Session Management**: Server-side sessions with secret key
- **Data Storage**: CSV files (patient_dataset.csv, nft_metadata.csv)
- **Blockchain**: Python-based simulation with SHA-256 hashing
- **Authentication**: Ethereum address verification with role mapping
- **ML Libraries**: scikit-learn, pandas, numpy

### Frontend Stack
- **Templates**: Jinja2 (server-side rendering)
- **Styling**: Bootstrap 5 + Custom CSS
- **Charts**: Chart.js for real-time visualizations
- **Web3**: ethers.js for MetaMask integration
- **AJAX**: Axios for API calls

### Security Features
- **Address Verification**: Every page load validates MetaMask address
- **Session Clearing**: Automatic logout on account change
- **Role-Based Decorators**: `@require_auth()` on protected routes
- **Data Filtering**: Backend filters all queries by authenticated role
- **CORS Protection**: Configured for localhost only

### Data Flow
```
1. Patient → NFT Consent Update → Blockchain Transaction
2. Blockchain → NFT Metadata CSV → Hospital Filtered Datasets
3. FL Engine → Load Consented Data → Local Training
4. Hospital Nodes → Send Model Updates → Server Aggregation
5. Server → FedAvg Algorithm → Global Model Update
6. Dashboard → Real-time Metrics → User Interface
```

---

## 6. Setup and Installation

### Prerequisites
- Python installed (v3.8 or higher)
- Git
- Node.js and npm (for Ganache authentication)
- MetaMask browser extension (for authentication)

### Quick Start Commands

**Option 1: Basic Setup (No Authentication)**
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

**Option 2: With Ganache Authentication (Recommended)**
```bash
# Terminal 1: Start Ganache
ganache --accounts 30 --port 7545 --deterministic

# Terminal 2: Setup and run Flask
pip install -r requirements.txt
python generate_address_mappings.py
python app.py
# Open http://localhost:5000/login and connect MetaMask
```

### Detailed Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Varshith-BR/Federated-Learning-on-NFT-Owned-Patient-Data.git
    cd Federated-Learning-on-NFT-Owned-Patient-Data
    ```

2.  **Create Virtual Environment** (Optional but Recommended)
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    python app.py
    ```

5.  **Access the Dashboard**
    - Open browser to `http://localhost:5000`

### 6.1 Ganache Authentication Setup (For Address-Based Access Control)

This project includes an **Ethereum address-based authentication system** using Ganache for role-based access control.

#### Prerequisites
- Node.js and npm installed
- MetaMask browser extension

#### Setup Steps

1.  **Install Ganache**
    ```bash
    npm install -g ganache
    ```

2.  **Start Ganache** (with deterministic addresses)
    ```bash
    ganache --accounts 30 --port 7545 --deterministic
    ```

3.  **Generate Address Mappings**
    ```bash
    python generate_address_mappings.py
    ```
    This creates `address_mapping.csv` with 30 pre-mapped accounts:
    - **Accounts 0-1**: Admins (full access)
    - **Accounts 2-9**: Hospitals (filtered data access)
    - **Accounts 10-29**: Patients (own records only)

4.  **Configure MetaMask**
    - Add network: `http://127.0.0.1:7545` (Chain ID: 1337)
    - Import test account private keys from Ganache

5.  **Access with Authentication**
    - Navigate to `http://localhost:5000/login`
    - Connect MetaMask wallet
    - System auto-detects role and redirects to appropriate portal

#### Role-Based Access
- **Admin** → `/training` (FL Training Dashboard)
- **Hospital** → `/hospital` (Hospital Portal with filtered data)
- **Patient** → `/patient` (Patient Portal with own records)

**📚 Detailed Documentation:** See `docs/` folder for comprehensive guides:
- `QUICK_START_AUTH.md` - Quick setup guide
- `GANACHE_AUTH_GUIDE.md` - Complete address mappings and private keys
- `URL_ACCESS_GUIDE.md` - All available endpoints
- `TEST_ACCOUNT_SWITCHING.md` - Testing instructions

---

## 7. Results & Observations

### 7.1 Model Performance (Real sklearn Training)

| Model | Training Accuracy | Validation Accuracy | Training Time |
|-------|------------------|---------------------|---------------|
| **Random Forest** | 100% | **95.60%** | ~2 seconds/round |
| **Neural Network (Deep MLP)** | ~98% | **~92%** | ~3 seconds/round |
| **Gradient Boosting** | ~99% | **~94%** | ~4 seconds/round |

### 7.2 Federated Learning Metrics
- **Participating Nodes**: 8 hospitals (all participating in each round)
- **Total Consented Data**: ~6,569 patient records per round
- **Global Model Convergence**: Stable after 2-3 rounds
- **Per-Hospital Accuracy Range**: 90-98% (varies by local data distribution)

### 7.3 Privacy & Consent
- **Privacy Preservation**: Zero leakage of raw patient rows between nodes.
- **Dynamic Consent**: Changes in the Patient Portal are immediately reflected in the next training round (verified via logs).
- **Consent Rate**: ~68.56% average across all hospitals
- **Blockchain Overhead**: Minimal impact on training start times (~1-2 seconds) due to efficient local simulation.

---

## 8. Future Scope

1.  **Integration with Ethereum/Hyperledger**: Replace the Python simulation with a real Web3 provider (Infura/Alchemy) and Solidity contracts.
2.  **Homomorphic Encryption**: Encrypt model weights during transit to prevent reverse-engineering of updates.
3.  **Mobile App**: Develop a React Native app for patients to manage consent on the go.
4.  **Differential Privacy**: Add noise to local updates to further guarantee individual privacy ($(\epsilon, \delta)$-differential privacy).

---

## 9. Conclusion

This project successfully demonstrates a working prototype of a privacy-first healthcare AI system. By empowering patients with NFT-based ownership, we bridge the trust gap between individuals and research institutions, paving the way for ethical and collaborative medical advancements.

---

**Developed for Major Project 2025**
*Contributors: Varshith B R*
