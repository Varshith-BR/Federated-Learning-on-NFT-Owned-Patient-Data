"""
Fetch addresses directly from running Ganache and create proper mappings
"""

import requests
import pandas as pd
import json

def get_ganache_addresses():
    """Fetch addresses from running Ganache RPC"""
    url = "http://127.0.0.1:7545"
    
    # Request accounts from Ganache
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_accounts",
        "params": [],
        "id": 1
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if 'result' in data:
            addresses = data['result']
            print(f"✅ Retrieved {len(addresses)} addresses from Ganache")
            return addresses
        else:
            print(f"❌ Error: {data}")
            return None
    except Exception as e:
        print(f"❌ Failed to connect to Ganache: {e}")
        print("Make sure Ganache is running on port 7545")
        return None

def create_address_mapping_from_ganache():
    """Create address mapping using actual Ganache addresses"""
    
    addresses = get_ganache_addresses()
    
    if not addresses or len(addresses) < 30:
        print("❌ Could not retrieve enough addresses from Ganache")
        print("Make sure Ganache is running with: ganache --accounts 30 --port 7545 --deterministic")
        return None
    
    print("\n📋 Ganache Addresses:")
    for i, addr in enumerate(addresses[:30]):
        print(f"  [{i}] {addr}")
    
    mappings = []
    
    # Admin accounts (index 0-1)
    mappings.append({
        'address': addresses[0],
        'role': 'admin',
        'entity_id': 'admin_001',
        'entity_name': 'FL System Administrator',
        'description': 'Full access to all portals and training controls'
    })
    
    mappings.append({
        'address': addresses[1],
        'role': 'admin',
        'entity_id': 'admin_002',
        'entity_name': 'Research Coordinator',
        'description': 'Full access to FL training and analytics'
    })
    
    # Hospital accounts (index 2-9)
    hospitals = [
        ('node_metro_general', 'Metro General Hospital'),
        ('node_regional', 'Regional Healthcare System'),
        ('node_st_marys', "St. Mary's Hospital"),
        ('node_university', 'University Medical Center'),
        ('node_community', 'Community Health Network'),
        ('node_city', 'City Medical Center'),
        ('node_veterans', 'Veterans Affairs Hospital'),
        ('node_childrens', "Children's Medical Center")
    ]
    
    for i, (node_id, hospital_name) in enumerate(hospitals):
        mappings.append({
            'address': addresses[i + 2],
            'role': 'hospital',
            'entity_id': node_id,
            'entity_name': hospital_name,
            'description': f'Access to {hospital_name} patient data only'
        })
    
    # Patient accounts (index 10-29) - 20 patients
    try:
        patient_df = pd.read_csv('patient_dataset.csv')
        sample_patients = patient_df.head(20)
        
        for i, (idx, patient) in enumerate(sample_patients.iterrows()):
            mappings.append({
                'address': addresses[i + 10],
                'role': 'patient',
                'entity_id': patient['patient_id'],
                'entity_name': patient.get('name', f"Patient {patient['patient_id']}"),
                'description': f"Patient data for {patient['patient_id']}"
            })
    except FileNotFoundError:
        print("⚠️ patient_dataset.csv not found, creating placeholder mappings")
        for i in range(20):
            mappings.append({
                'address': addresses[i + 10],
                'role': 'patient',
                'entity_id': f'P{str(i+1).zfill(6)}',
                'entity_name': f'Patient Demo {i+1}',
                'description': f'Demo patient account {i+1}'
            })
    
    # Create DataFrame and save
    df = pd.DataFrame(mappings)
    df.to_csv('address_mapping.csv', index=False)
    
    print(f"\n✅ Created {len(df)} address mappings")
    print(f"   - Admins: {len(df[df['role'] == 'admin'])}")
    print(f"   - Hospitals: {len(df[df['role'] == 'hospital'])}")
    print(f"   - Patients: {len(df[df['role'] == 'patient'])}")
    
    return df

def update_nft_metadata():
    """Update NFT metadata with actual Ganache addresses"""
    try:
        mapping_df = pd.read_csv('address_mapping.csv')
        nft_df = pd.read_csv('nft_metadata.csv')
        
        patient_mappings = mapping_df[mapping_df['role'] == 'patient'][['entity_id', 'address']]
        patient_mappings.columns = ['patient_id', 'wallet_address']
        
        nft_df = nft_df.merge(patient_mappings, on='patient_id', how='left', suffixes=('_old', ''))
        
        if 'wallet_id' in nft_df.columns:
            nft_df['wallet_address'] = nft_df['wallet_address'].fillna(nft_df['wallet_id'])
            nft_df.drop(columns=['wallet_id'], inplace=True)
        
        nft_df['wallet_address'] = nft_df['wallet_address'].fillna(nft_df.get('wallet_address_old', '0x0000000000000000000000000000000000000000'))
        
        if 'wallet_address_old' in nft_df.columns:
            nft_df.drop(columns=['wallet_address_old'], inplace=True)
        
        nft_df.rename(columns={'wallet_address': 'wallet_id'}, inplace=True)
        nft_df.to_csv('nft_metadata.csv', index=False)
        
        print(f"✅ Updated NFT metadata with Ganache addresses")
        
    except Exception as e:
        print(f"❌ Error updating NFT metadata: {e}")

def print_account_info():
    """Print account information for easy reference"""
    mapping_df = pd.read_csv('address_mapping.csv')
    
    print("\n" + "="*80)
    print("GANACHE ACCOUNT MAPPINGS")
    print("="*80)
    
    print("\n🔐 ADMIN ACCOUNTS")
    admins = mapping_df[mapping_df['role'] == 'admin']
    for idx, admin in admins.iterrows():
        print(f"\n  {admin['entity_name']}")
        print(f"  Address: {admin['address']}")
        print(f"  Access: {admin['description']}")
    
    print("\n\n🏥 HOSPITAL ACCOUNTS")
    hospitals = mapping_df[mapping_df['role'] == 'hospital']
    for idx, hospital in hospitals.iterrows():
        print(f"\n  {hospital['entity_name']}")
        print(f"  Address: {hospital['address']}")
        print(f"  Node ID: {hospital['entity_id']}")
    
    print("\n\n👤 PATIENT ACCOUNTS")
    patients = mapping_df[mapping_df['role'] == 'patient']
    for idx, patient in patients.iterrows():
        print(f"\n  {patient['entity_name']}")
        print(f"  Address: {patient['address']}")
        print(f"  Patient ID: {patient['entity_id']}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    print("🔧 Fetching addresses from Ganache...\n")
    
    df = create_address_mapping_from_ganache()
    
    if df is not None:
        print("\n🔄 Updating NFT metadata...")
        update_nft_metadata()
        
        print("\n📊 Account Information:")
        print_account_info()
        
        print("\n✅ Setup complete!")
        print("\n⚠️  IMPORTANT: Restart Flask app (Ctrl+C and run 'python app.py') to reload mappings")
    else:
        print("\n❌ Setup failed. Please ensure Ganache is running.")
