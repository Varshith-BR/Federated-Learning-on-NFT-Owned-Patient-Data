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
- **Core Engine**: `federated_learning_engine.py` & `app.py` (Simulation)
- **Models Supported**: 
    - **Logistic Regression**: For binary classification tasks.
    - **Neural Networks (MLP)**: For complex pattern recognition.
    - **Support Vector Machines (SVM)**: For robust classification.
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

The system supports three distinct model architectures to handle various healthcare prediction tasks:

### 4.1 Logistic Regression
- **Type**: Linear Model
- **Usage**: Primary for binary classification tasks (e.g., presence vs. absence of disease).
- **Configuration**:
    - **Solver**: L-BFGS (Limited-memory Broyden–Fletcher–Goldfarb–Shanno).
    - **Max Iterations**: 1000 for convergence.
    - **Features**: Highly interpretable, lightweight, and efficient for initial benchmarks.
- **Why it's used**: Provides a baseline for performance; essential for scenarios requiring explainability in medical decisions.

### 4.2 Neural Network (Multi-Layer Perceptron)
- **Type**: Deep Learning Classifier
- **Architecture**:
    - **Input Layer**: Matches feature dimension derived from patient records.
    - **Hidden Layers**: Two dense layers with **100** and **50** units respectively.
    - **Activation Function**: ReLU (Rectified Linear Unit) for non-linearity.
- **Configuration**:
    - **Optimizer**: Adam (Adaptive Moment Estimation).
    - **Max Iterations**: 500.
- **Why it's used**: Captures complex, non-linear relationships in patient data that simpler models might miss, offering higher potential accuracy for complex diagnoses.

### 4.3 Support Vector Machine (SVM)
- **Type**: Kernel-based Classifier
- **Configuration**:
    - **Kernel**: RBF (Radial Basis Function) to handle non-linear decision boundaries.
    - **Probability Estimates**: Enabled (computationally expensive but necessary for confidence scores).
    - **Regularization**: Optimized to prevent overfitting on smaller hospital datasets.
- **Why it's used**: Effective in high-dimensional spaces and robust even when the number of dimensions exceeds the number of samples, common in specific genomic or rare-disease datasets.

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

## 6. Setup and Installation

### Prerequisites
- Python installed (v3.8 or higher)
- Git

### Steps
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

---

## 7. Results & Observations

- **Privacy Preservation**: Zero leakage of raw patient rows between nodes.
- **Dynamic Consent**: Changes in the Patient Portal are immediately reflected in the next training round (verified via logs).
- **Model Performance**: 
    - **Logistic Regression**: Reached ~85% accuracy within 5 rounds on synthetic data.
    - **Neural Networks**: Showed higher adaptability (~89% accuracy) but required more computation time.
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

**Developed for Major Project 2024**
*Contributors:Varshith B R*
