# Blockchain & Smart Contract Architecture

## Overview
This project uses a **Hybrid Architecture** to balance performance with decentralized security principles.

### 1. The Simulation Layer (Python)
For the purpose of this demonstration and rapid prototyping, the blockchain ledger is simulated in `blockchain_nft_system.py`. 
- **Why?** Running a full Ethereum node or Testnet interactions introduces latency (15s+ per block) and requires gas fees, which disrupts the user experience of the Federated Learning demo.
- **How?** The `BlockchainNetwork` class maintains an immutable chain of `Block` objects, cryptographically linked via SHA-256 hashes, behaving exactly like a real blockchain.

### 2. The Smart Contract Layer (Solidity)
The file `contracts/PatientConsent.sol` represents the **production-ready code** that would be deployed to the Ethereum Mainnet or Polygon.

- **Standard**: ERC-721 (Non-Fungible Token)
- **Logic**: 
    - Each patient data profile is minted as a unique NFT.
    - Ownership of the NFT = Ownership of the Data.
    - The `updateConsent` function ensures that **only the wallet holding the NFT** can authorize data usage.

### 3. Verification & Transparency (New)
A built-in **Blockchain Explorer** (`/blockchain`) visualizes the simulated ledger in real-time, showing:
- Block Hashes (SHA-256)
- Linking of Previous Hashes (Merkle Chain)
- Timestamps and Nonces

## Engineering Standards
The project includes industry-standard configuration files to demonstrate readiness for Mainnet deployment:
- `hardhat.config.js`: Configuration for Ethereum development environment.
- `scripts/deploy.js`: Automation scripts for contract deployment.
- `test/`: Unit tests ensuring contract security and logic.

## Smart Contract Functions

| Function | Description |
|----------|-------------|
| `mintConsentNFT` | Issues a new Data NFT to a patient's wallet address. |
| `updateConsent` | Called by the patient to Grant/Revoke training permissions. |
| `isConsentValid` | Called by the FL Server to verify permission on-chain before training. |

## Verification Flow
1. **User Action**: Patient clicks "Update Consent" in the web portal.
2. **Crypto Auth**: MetaMask prompts the user to **Sign** the request.
3. **Execution**: The backend verifies this signature (mirroring the transaction validation that would happen on-chain).
