
import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pandas as pd


class Block:
    """Individual block in the blockchain"""

    def __init__(self, index: int, transactions: List[dict], timestamp: float, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int = 1):
        """Simple proof-of-work mining"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    def to_dict(self) -> dict:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class PatientNFT:
    """NFT representation of patient data ownership"""

    def __init__(self, patient_id: str, wallet_address: str, metadata: dict):
        self.patient_id = patient_id
        self.wallet_address = wallet_address
        self.metadata = metadata
        self.token_id = self.generate_token_id()
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def generate_token_id(self) -> str:
        """Generate unique token ID for the NFT"""
        token_string = f"{self.patient_id}_{self.wallet_address}_{time.time()}"
        return hashlib.sha256(token_string.encode()).hexdigest()[:16]

    def update_consent(self, allow_training: bool, expiry_date: Optional[str] = None):
        """Update consent status in NFT metadata"""
        self.metadata['allow_training'] = allow_training
        self.metadata['consent_timestamp'] = datetime.now().isoformat()
        if expiry_date:
            self.metadata['expiry_date'] = expiry_date
        self.updated_at = datetime.now().isoformat()

    def is_consent_valid(self) -> Tuple[bool, str]:
        """Check if consent is currently valid"""
        if not self.metadata.get('allow_training', False):
            return False, "Consent not granted"

        expiry_date = self.metadata.get('expiry_date')
        if expiry_date:
            expiry = datetime.fromisoformat(expiry_date.replace('Z', ''))
            if expiry <= datetime.now():
                return False, "Consent expired"

        return True, "Valid consent"

    def to_dict(self) -> dict:
        """Convert NFT to dictionary"""
        return {
            'token_id': self.token_id,
            'patient_id': self.patient_id,
            'wallet_address': self.wallet_address,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class SmartContract:
    """Smart contract for consent management"""

    def __init__(self, contract_address: str):
        self.contract_address = contract_address
        self.nft_registry: Dict[str, PatientNFT] = {}
        self.consent_logs: List[dict] = []

    def mint_nft(self, patient_id: str, wallet_address: str, metadata: dict) -> str:
        """Mint a new patient NFT"""
        nft = PatientNFT(patient_id, wallet_address, metadata)
        self.nft_registry[nft.token_id] = nft

        # Log the minting transaction
        self.consent_logs.append({
            'action': 'mint',
            'token_id': nft.token_id,
            'patient_id': patient_id,
            'wallet_address': wallet_address,
            'timestamp': datetime.now().isoformat()
        })

        return nft.token_id

    def update_consent(self, token_id: str, allow_training: bool, expiry_date: Optional[str] = None) -> bool:
        """Update consent for an NFT"""
        if token_id not in self.nft_registry:
            return False

        nft = self.nft_registry[token_id]
        old_consent = nft.metadata.get('allow_training', False)

        nft.update_consent(allow_training, expiry_date)

        # Log the consent update
        self.consent_logs.append({
            'action': 'consent_update',
            'token_id': token_id,
            'patient_id': nft.patient_id,
            'old_consent': old_consent,
            'new_consent': allow_training,
            'expiry_date': expiry_date,
            'timestamp': datetime.now().isoformat()
        })

        return True

    def get_nft(self, token_id: str) -> Optional[PatientNFT]:
        """Get NFT by token ID"""
        return self.nft_registry.get(token_id)

    def get_nft_by_patient(self, patient_id: str) -> Optional[PatientNFT]:
        """Get NFT by patient ID"""
        for nft in self.nft_registry.values():
            if nft.patient_id == patient_id:
                return nft
        return None

    def verify_consent(self, patient_id: str) -> Tuple[bool, str]:
        """Verify patient consent for training"""
        nft = self.get_nft_by_patient(patient_id)
        if not nft:
            return False, "NFT not found"

        return nft.is_consent_valid()

    def get_consent_statistics(self) -> dict:
        """Get consent statistics across all NFTs"""
        total_nfts = len(self.nft_registry)
        consented_count = 0
        expired_count = 0

        for nft in self.nft_registry.values():
            is_valid, reason = nft.is_consent_valid()
            if is_valid:
                consented_count += 1
            elif "expired" in reason.lower():
                expired_count += 1

        return {
            'total_nfts': total_nfts,
            'consented_count': consented_count,
            'expired_count': expired_count,
            'consent_rate': (consented_count / total_nfts) if total_nfts > 0 else 0
        }


class BlockchainNetwork:
    """Simulated blockchain network for NFT consent management"""

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[dict] = []
        self.smart_contracts: Dict[str, SmartContract] = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Get the latest block in the chain"""
        return self.chain[-1]

    def deploy_smart_contract(self, contract_address: str) -> str:
        """Deploy a new smart contract"""
        contract = SmartContract(contract_address)
        self.smart_contracts[contract_address] = contract

        # Add deployment transaction
        self.pending_transactions.append({
            'type': 'contract_deployment',
            'contract_address': contract_address,
            'timestamp': datetime.now().isoformat()
        })

        return contract_address

    def get_smart_contract(self, contract_address: str) -> Optional[SmartContract]:
        """Get smart contract by address"""
        return self.smart_contracts.get(contract_address)

    def add_transaction(self, transaction: dict):
        """Add a transaction to the pending pool"""
        transaction['timestamp'] = datetime.now().isoformat()
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, mining_reward_address: str = "system"):
        """Mine all pending transactions into a new block"""
        if not self.pending_transactions:
            return None

        # Add mining reward transaction
        reward_transaction = {
            'type': 'mining_reward',
            'recipient': mining_reward_address,
            'amount': 10,  # Arbitrary reward
            'timestamp': datetime.now().isoformat()
        }
        self.pending_transactions.append(reward_transaction)

        # Create new block
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            timestamp=time.time(),
            previous_hash=self.get_latest_block().hash
        )

        # Mine the block (simple proof-of-work)
        new_block.mine_block(difficulty=2)

        # Add to chain and clear pending transactions
        self.chain.append(new_block)
        self.pending_transactions = []

        return new_block

    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_chain_info(self) -> dict:
        """Get information about the blockchain"""
        return {
            'total_blocks': len(self.chain),
            'total_transactions': sum(len(block.transactions) for block in self.chain),
            'total_contracts': len(self.smart_contracts),
            'chain_valid': self.is_chain_valid(),
            'latest_block_hash': self.get_latest_block().hash,
            'pending_transactions': len(self.pending_transactions)
        }


class NFTConsentManager:
    """High-level manager for NFT-based consent using blockchain"""

    def __init__(self):
        self.blockchain = BlockchainNetwork()
        self.contract_address = "0x" + hashlib.sha256("PatientConsentContract".encode()).hexdigest()[:40]

        # Deploy the consent management contract
        self.blockchain.deploy_smart_contract(self.contract_address)
        self.contract = self.blockchain.get_smart_contract(self.contract_address)

    def create_patient_nft(self, patient_id: str, patient_data: dict) -> str:
        """Create an NFT for patient data with consent metadata"""
        # Generate wallet address for patient
        wallet_address = "0x" + hashlib.sha256(f"patient_{patient_id}".encode()).hexdigest()[:40]

        # Create NFT metadata based on patient data
        metadata = {
            'patient_id': patient_id,
            'data_hash': hashlib.sha256(json.dumps(patient_data, sort_keys=True).encode()).hexdigest(),
            'allow_training': patient_data.get('allow_training', False),
            'consent_timestamp': datetime.now().isoformat(),
            'expiry_date': patient_data.get('expiry_date'),
            'hospital': patient_data.get('hospital', 'Unknown'),
            'created_by': 'system'
        }

        # Mint NFT
        token_id = self.contract.mint_nft(patient_id, wallet_address, metadata)

        # Add transaction to blockchain
        self.blockchain.add_transaction({
            'type': 'nft_mint',
            'contract_address': self.contract_address,
            'patient_id': patient_id,
            'token_id': token_id,
            'wallet_address': wallet_address
        })

        return token_id

    def update_patient_consent(self, patient_id: str, allow_training: bool, expiry_date: Optional[str] = None) -> bool:
        """Update patient consent through NFT"""
        nft = self.contract.get_nft_by_patient(patient_id)
        if not nft:
            return False

        # Update consent in smart contract
        success = self.contract.update_consent(nft.token_id, allow_training, expiry_date)

        if success:
            # Add transaction to blockchain
            self.blockchain.add_transaction({
                'type': 'consent_update',
                'contract_address': self.contract_address,
                'patient_id': patient_id,
                'token_id': nft.token_id,
                'allow_training': allow_training,
                'expiry_date': expiry_date
            })

        return success

    def verify_patient_consent(self, patient_id: str) -> Tuple[bool, str]:
        """Verify if patient has valid consent for training"""
        return self.contract.verify_consent(patient_id)

    def get_patient_nft_info(self, patient_id: str) -> Optional[dict]:
        """Get patient NFT information"""
        nft = self.contract.get_nft_by_patient(patient_id)
        if not nft:
            return None

        is_valid, reason = nft.is_consent_valid()

        return {
            'token_id': nft.token_id,
            'wallet_address': nft.wallet_address,
            'metadata': nft.metadata,
            'consent_valid': is_valid,
            'consent_reason': reason,
            'created_at': nft.created_at,
            'updated_at': nft.updated_at
        }

    def mine_transactions(self) -> Optional[dict]:
        """Mine pending transactions into blockchain"""
        block = self.blockchain.mine_pending_transactions()
        if block:
            return block.to_dict()
        return None

    def get_system_stats(self) -> dict:
        """Get comprehensive system statistics"""
        blockchain_info = self.blockchain.get_chain_info()
        consent_stats = self.contract.get_consent_statistics()

        return {
            'blockchain': blockchain_info,
            'consent': consent_stats,
            'contract_address': self.contract_address,
            'system_status': 'operational'
        }

    def export_audit_log(self) -> List[dict]:
        """Export complete audit log of all consent transactions"""
        return self.contract.consent_logs

    def initialize_from_csv_data(self, patient_csv_path: str, nft_csv_path: str) -> int:
        """Initialize NFTs from existing CSV data"""
        try:
            patient_df = pd.read_csv(patient_csv_path)
            nft_df = pd.read_csv(nft_csv_path)

            # Merge data
            merged_df = patient_df.merge(nft_df, on='patient_id', how='left')

            created_count = 0
            for i, (_, row) in enumerate(merged_df.iterrows()):
                patient_data = row.to_dict()
                token_id = self.create_patient_nft(row['patient_id'], patient_data)
                if token_id:
                    created_count += 1
                
                # Mine a block every 10 transactions to create a realistic chain
                if (i + 1) % 10 == 0:
                    self.mine_transactions()

            # Mine remaining transactions
            self.mine_transactions()

            return created_count

        except Exception as e:
            print(f"Error initializing from CSV: {e}")
            return 0


# Example usage and testing
if __name__ == "__main__":
    # Initialize NFT consent manager
    nft_manager = NFTConsentManager()

    # Test with sample patient data
    sample_patients = [
        {
            'patient_id': 'P000001',
            'age': 45,
            'hospital': 'Metro General Hospital',
            'allow_training': True,
            'expiry_date': '2025-12-31'
        },
        {
            'patient_id': 'P000002',
            'age': 32,
            'hospital': 'City Medical Center',
            'allow_training': False,
            'expiry_date': None
        }
    ]

    # Create NFTs for sample patients
    for patient_data in sample_patients:
        token_id = nft_manager.create_patient_nft(patient_data['patient_id'], patient_data)
        print(f"Created NFT for {patient_data['patient_id']}: {token_id}")

    # Mine transactions
    block = nft_manager.mine_transactions()
    print(f"Mined block: {block['index'] if block else 'None'}")

    # Test consent verification
    for patient_data in sample_patients:
        is_valid, reason = nft_manager.verify_patient_consent(patient_data['patient_id'])
        print(f"Patient {patient_data['patient_id']} consent: {is_valid} - {reason}")

    # Test consent update
    success = nft_manager.update_patient_consent('P000002', True, '2025-06-30')
    print(f"Updated consent for P000002: {success}")

    # Get system statistics
    stats = nft_manager.get_system_stats()
    print(f"System stats: {json.dumps(stats, indent=2)}")
