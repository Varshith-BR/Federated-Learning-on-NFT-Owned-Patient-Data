# Data Flow Diagrams

## NFT-Based Federated Learning System

This document provides comprehensive data flow diagrams for the implemented system, showing how data moves through different components and processes.

---

## 1. System Overview - High-Level Data Flow

```mermaid
flowchart TB
    subgraph Users["User Layer"]
        Patient["Patient<br/>(MetaMask)"]
        Hospital["Hospital Staff<br/>(MetaMask)"]
        Admin["Admin/Researcher<br/>(MetaMask)"]
    end
    
    subgraph WebApp["Flask Web Application"]
        Auth["Authentication<br/>Service"]
        API["REST API<br/>Gateway"]
        Session["Session<br/>Management"]
    end
    
    subgraph Backend["Application Layer"]
        FLEngine["Federated Learning<br/>Engine"]
        BlockchainSim["Blockchain<br/>Simulation"]
        NFTManager["NFT Consent<br/>Manager"]
    end
    
    subgraph DataLayer["Data Layer (CSV)"]
        PatientData["patient_dataset.csv"]
        NFTData["nft_metadata.csv"]
        NodeData["node_*.csv<br/>(8 hospitals)"]
        AddressMap["address_mapping.csv"]
    end
    
    Patient -->|Connect Wallet| Auth
    Hospital -->|Connect Wallet| Auth
    Admin -->|Connect Wallet| Auth
    
    Auth -->|Verify Address| AddressMap
    Auth -->|Create Session| Session
    Session -->|Authorize| API
    
    API -->|Update Consent| NFTManager
    API -->|Start Training| FLEngine
    API -->|Query Data| DataLayer
    
    NFTManager -->|Read/Write| NFTData
    NFTManager -->|Log Transaction| BlockchainSim
    
    FLEngine -->|Load Data| NodeData
    FLEngine -->|Verify Consent| NFTManager
    FLEngine -->|Filter Data| NodeData
    
    BlockchainSim -->|Audit Trail| API
    FLEngine -->|Training Results| API
    API -->|Response| Users
```

---

## 2. Authentication Flow

```mermaid
sequenceDiagram
    participant User as User Browser
    participant MM as MetaMask
    participant Flask as Flask App
    participant CSV as address_mapping.csv
    participant Session as Session Store
    
    User->>Flask: GET /login
    Flask->>User: Render login page
    User->>MM: Click "Connect Wallet"
    MM->>User: Request permission
    User->>MM: Approve connection
    MM->>User: Return address
    
    User->>Flask: POST /api/auth/verify<br/>{address}
    Flask->>CSV: Lookup address
    CSV->>Flask: Return role (admin/hospital/patient)
    Flask->>Session: Create session<br/>{address, role, user_id}
    Flask->>User: {success: true, role, redirect_url}
    
    User->>Flask: Navigate to portal
    Flask->>Session: Validate session
    Session->>Flask: Session valid
    Flask->>User: Render portal (role-based)
```

---

## 3. Patient Consent Update Flow

```mermaid
flowchart TD
    Start([Patient Opens Portal]) --> Auth{Authenticated?}
    Auth -->|No| Login[Redirect to Login]
    Auth -->|Yes| LoadData[Load Patient Data<br/>from CSV]
    
    LoadData --> Display[Display Current<br/>Consent Status]
    Display --> UserAction{User Action}
    
    UserAction -->|Toggle Consent| UpdateForm[Update Consent Form]
    UserAction -->|Set Expiry| UpdateForm
    
    UpdateForm --> Submit[Submit Changes]
    Submit --> Validate{Validate<br/>Input}
    
    Validate -->|Invalid| Error[Show Error]
    Error --> Display
    
    Validate -->|Valid| UpdateNFT[Update NFT Metadata]
    UpdateNFT --> WriteCSV[Write to<br/>nft_metadata.csv]
    WriteCSV --> CreateTx[Create Blockchain<br/>Transaction]
    
    CreateTx --> LogBlock[Add to Blockchain<br/>Ledger]
    LogBlock --> UpdateNodes[Update Hospital<br/>Node CSVs]
    
    UpdateNodes --> Success[Show Success<br/>Message]
    Success --> Refresh[Refresh Dashboard]
    Refresh --> Display
```

---

## 4. Federated Learning Training Flow

```mermaid
sequenceDiagram
    participant Admin as Admin Portal
    participant API as Flask API
    participant FLServer as FL Server
    participant Nodes as Hospital Nodes (8)
    participant NFT as NFT Manager
    participant CSV as CSV Files
    participant Blockchain as Blockchain Sim
    
    Admin->>API: POST /api/start_training<br/>{model_type, rounds, mode}
    API->>FLServer: Initialize training
    FLServer->>FLServer: Create global model
    
    loop For each training round
        FLServer->>Nodes: Broadcast global model
        
        par Parallel Local Training
            Nodes->>CSV: Load local data
            Nodes->>NFT: Get consent status
            NFT->>CSV: Read nft_metadata.csv
            CSV->>NFT: Return consent data
            NFT->>Nodes: Return consented patients
            
            Nodes->>Nodes: Filter data by consent
            Nodes->>Nodes: Train local model
            Nodes->>FLServer: Send model updates
        end
        
        FLServer->>FLServer: Aggregate updates (FedAvg)
        FLServer->>FLServer: Update global model
        FLServer->>Blockchain: Log training round
        FLServer->>API: Update training status
        API->>Admin: Push real-time metrics
    end
    
    FLServer->>API: Training complete
    API->>Admin: Show final results
```

---

## 5. Consent Filtering Process

```mermaid
flowchart LR
    subgraph Input["Input Data"]
        AllData["All Patient Records<br/>at Hospital Node"]
    end
    
    subgraph ConsentCheck["Consent Verification"]
        LoadNFT["Load NFT Metadata<br/>for each patient"]
        CheckAllow{allow_training<br/>= true?}
        CheckExpiry{expiry_date<br/>> current_time?}
    end
    
    subgraph Output["Output Data"]
        Consented["Consented Data<br/>D_filtered"]
        Excluded["Excluded Data<br/>(Not used)"]
    end
    
    AllData --> LoadNFT
    LoadNFT --> CheckAllow
    
    CheckAllow -->|No| Excluded
    CheckAllow -->|Yes| CheckExpiry
    
    CheckExpiry -->|Expired| Excluded
    CheckExpiry -->|Valid/No Expiry| Consented
    
    Consented --> Training["Used for<br/>Local Training"]
    Excluded --> Discard["Discarded<br/>(Privacy Protected)"]
```

---

## 6. Hospital Portal Data Access Flow

```mermaid
flowchart TD
    Start([Hospital User Login]) --> Auth[Authenticate via MetaMask]
    Auth --> GetRole[Get Role from<br/>address_mapping.csv]
    GetRole --> CheckRole{Role = Hospital?}
    
    CheckRole -->|No| Deny[Access Denied]
    CheckRole -->|Yes| GetHospital[Extract hospital_id<br/>from mapping]
    
    GetHospital --> LoadData[Load Data Sources]
    
    LoadData --> FilterPatients[Filter patient_dataset.csv<br/>WHERE hospital = hospital_id]
    LoadData --> LoadNode[Load node_hospital_name.csv]
    LoadData --> LoadNFT[Load nft_metadata.csv]
    
    FilterPatients --> JoinData[Join Patient + NFT Data]
    LoadNode --> JoinData
    LoadNFT --> JoinData
    
    JoinData --> CalcStats[Calculate Statistics:<br/>- Total patients<br/>- Consented count<br/>- Data distribution]
    
    CalcStats --> Render[Render Hospital Portal<br/>with filtered data]
    Render --> Display([Display Dashboard])
```

---

## 7. Blockchain Transaction Flow

```mermaid
sequenceDiagram
    participant User as User Action
    participant NFTMgr as NFT Manager
    participant BC as Blockchain Network
    participant TxPool as Transaction Pool
    participant Block as Block
    participant Chain as Blockchain Chain
    
    User->>NFTMgr: Update consent
    NFTMgr->>NFTMgr: Create transaction object<br/>{type, patient_id, data, timestamp}
    NFTMgr->>BC: Add transaction
    
    BC->>TxPool: Add to pending pool
    TxPool->>TxPool: Queue transaction
    
    BC->>BC: Mine pending transactions
    BC->>Block: Create new block<br/>{index, transactions, prev_hash}
    Block->>Block: Calculate hash (SHA-256)
    Block->>Block: Proof-of-work mining
    
    Block->>Chain: Append to chain
    Chain->>Chain: Validate chain integrity
    Chain->>BC: Confirm block added
    
    BC->>NFTMgr: Transaction confirmed
    NFTMgr->>User: Success response
```

---

## 8. Model Aggregation Flow (FedAvg)

```mermaid
flowchart TB
    subgraph Round["Training Round t"]
        direction TB
        
        subgraph Nodes["Hospital Nodes"]
            N1["Node 1<br/>n1 samples<br/>w1 weights"]
            N2["Node 2<br/>n2 samples<br/>w2 weights"]
            N3["Node 3<br/>n3 samples<br/>w3 weights"]
            N8["Node 8<br/>n8 samples<br/>w8 weights"]
        end
        
        subgraph Server["FL Server"]
            Collect[Collect Local Updates]
            CalcWeights["Calculate Weights:<br/>weight_k = n_k / Σn_k"]
            Aggregate["Aggregate:<br/>W_global = Σ(weight_k × w_k)"]
            Update[Update Global Model]
        end
        
        N1 --> Collect
        N2 --> Collect
        N3 --> Collect
        N8 --> Collect
        
        Collect --> CalcWeights
        CalcWeights --> Aggregate
        Aggregate --> Update
    end
    
    Update --> NextRound{More<br/>Rounds?}
    NextRound -->|Yes| Broadcast[Broadcast W_global<br/>to all nodes]
    NextRound -->|No| Complete[Training Complete]
    
    Broadcast --> Round
```

---

## 9. Complete End-to-End Training Workflow

```mermaid
flowchart TD
    Start([Admin Initiates Training]) --> Config[Configure Parameters:<br/>- Model type<br/>- Number of rounds<br/>- Privacy mode]
    
    Config --> InitModel[Initialize Global Model<br/>W_0]
    InitModel --> StartRound[Start Round t]
    
    StartRound --> Broadcast[Broadcast W_t to Nodes]
    
    Broadcast --> Node1[Node 1: Load Data]
    Broadcast --> Node2[Node 2: Load Data]
    Broadcast --> Node8[Node 8: Load Data]
    
    Node1 --> Filter1[Apply Consent Filter]
    Node2 --> Filter2[Apply Consent Filter]
    Node8 --> Filter8[Apply Consent Filter]
    
    Filter1 --> Train1[Local Training]
    Filter2 --> Train2[Local Training]
    Filter8 --> Train8[Local Training]
    
    Train1 --> Send1[Send w_1]
    Train2 --> Send2[Send w_2]
    Train8 --> Send8[Send w_8]
    
    Send1 --> Aggregate[Server: FedAvg]
    Send2 --> Aggregate
    Send8 --> Aggregate
    
    Aggregate --> UpdateGlobal[Update W_global]
    UpdateGlobal --> Evaluate[Evaluate Performance]
    
    Evaluate --> Log[Log Metrics:<br/>- Accuracy<br/>- Loss<br/>- Participants]
    
    Log --> CheckRounds{t < max_rounds?}
    CheckRounds -->|Yes| IncRound[t = t + 1]
    IncRound --> StartRound
    
    CheckRounds -->|No| SaveModel[Save Final Model]
    SaveModel --> Complete([Training Complete])
```

---

## 10. Data Layer Relationships

```mermaid
erDiagram
    PATIENT_DATASET ||--o{ NFT_METADATA : "has"
    PATIENT_DATASET ||--o{ NODE_DATA : "distributed_to"
    NFT_METADATA ||--|| BLOCKCHAIN : "recorded_in"
    ADDRESS_MAPPING ||--o{ PATIENT_DATASET : "maps_to"
    ADDRESS_MAPPING ||--o{ HOSPITAL_NODES : "maps_to"
    
    PATIENT_DATASET {
        string patient_id PK
        string name
        int age
        string gender
        string hospital
        string primary_condition
        string medications
        float lab_results
    }
    
    NFT_METADATA {
        string patient_id PK
        string token_id
        string wallet_address
        bool allow_training
        datetime expiry_date
        datetime last_updated
    }
    
    NODE_DATA {
        string patient_id PK
        string hospital FK
        string medical_data
        bool consent_status
    }
    
    ADDRESS_MAPPING {
        string ethereum_address PK
        string role
        string user_id
        string hospital_name
    }
    
    BLOCKCHAIN {
        int block_index PK
        string block_hash
        string previous_hash
        array transactions
        datetime timestamp
    }
    
    HOSPITAL_NODES {
        string hospital_id PK
        string hospital_name
        int total_patients
        int consented_patients
        string data_file_path
    }
```

---

## 11. Privacy-Preserving Data Flow

```mermaid
flowchart LR
    subgraph Hospital1["Hospital 1"]
        Raw1["Raw Patient Data<br/>(Never Shared)"]
        Filter1["Consent Filter"]
        Local1["Local Model<br/>Training"]
        Params1["Model Parameters<br/>(Weights Only)"]
    end
    
    subgraph Hospital2["Hospital 2"]
        Raw2["Raw Patient Data<br/>(Never Shared)"]
        Filter2["Consent Filter"]
        Local2["Local Model<br/>Training"]
        Params2["Model Parameters<br/>(Weights Only)"]
    end
    
    subgraph Server["Central Server"]
        Aggregate["Federated<br/>Averaging"]
        Global["Global Model<br/>W_global"]
    end
    
    Raw1 -.->|Never Leaves| Filter1
    Filter1 --> Local1
    Local1 --> Params1
    Params1 -->|Encrypted| Aggregate
    
    Raw2 -.->|Never Leaves| Filter2
    Filter2 --> Local2
    Local2 --> Params2
    Params2 -->|Encrypted| Aggregate
    
    Aggregate --> Global
    Global -.->|Broadcast| Hospital1
    Global -.->|Broadcast| Hospital2
    
    style Raw1 fill:#ffcccc
    style Raw2 fill:#ffcccc
    style Params1 fill:#ccffcc
    style Params2 fill:#ccffcc
```

---

## 12. Real-Time Dashboard Update Flow

```mermaid
sequenceDiagram
    participant Browser as User Browser
    participant Flask as Flask Server
    participant FLEngine as FL Engine
    participant Status as Training Status
    
    Browser->>Flask: Load training dashboard
    Flask->>Browser: Render page with Chart.js
    
    Browser->>Browser: Start polling interval (2s)
    
    loop Every 2 seconds
        Browser->>Flask: GET /api/training_status
        Flask->>Status: Read current status
        Status->>Flask: {is_training, round, progress, metrics}
        Flask->>Browser: JSON response
        Browser->>Browser: Update charts and metrics
    end
    
    Note over FLEngine: Training completes
    FLEngine->>Status: Update status<br/>{is_training: false}
    
    Browser->>Flask: GET /api/training_status
    Flask->>Status: Read status
    Status->>Flask: {is_training: false, final_metrics}
    Flask->>Browser: Training complete
    Browser->>Browser: Stop polling<br/>Show final results
```

---

## Summary

These diagrams illustrate:

1. **System Overview**: High-level component interactions
2. **Authentication**: MetaMask wallet-based login flow
3. **Consent Management**: Patient consent update process
4. **Federated Learning**: Complete training workflow
5. **Consent Filtering**: Privacy-preserving data selection
6. **Hospital Portal**: Role-based data access
7. **Blockchain**: Transaction and block creation
8. **Model Aggregation**: FedAvg algorithm implementation
9. **End-to-End Training**: Complete training lifecycle
10. **Data Relationships**: CSV file structure and relationships
11. **Privacy Flow**: Data isolation and parameter sharing
12. **Real-Time Updates**: Dashboard polling mechanism

All diagrams are based on the actual implemented system architecture.

---

**Document Version**: 1.0  
**Last Updated**: December 9, 2025  
**Format**: Mermaid diagrams (rendered in Markdown viewers)
