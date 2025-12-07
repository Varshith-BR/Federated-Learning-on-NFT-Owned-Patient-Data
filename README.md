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

## 2. System Architecture

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

## 4. Tools & Technologies

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
*Contributors: [Your Name/Team Name]*
