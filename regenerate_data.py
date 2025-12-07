
import pandas as pd
import glob
import os

def regenerate_data():
    print("Searching for node data files...")
    # Find all node data files
    node_files = glob.glob('node_*_filtered_data.csv')
    
    if not node_files:
        print("Error: No node data files found!")
        return

    print(f"Found {len(node_files)} node files: {node_files}")

    all_data = []
    
    for file in node_files:
        try:
            print(f"Reading {file}...")
            df = pd.read_csv(file)
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not all_data:
        print("No data loaded.")
        return

    # Concatenate all data
    full_dataset = pd.concat(all_data, ignore_index=True)
    print(f"Total records aggregated: {len(full_dataset)}")

    # Save patient_dataset.csv (Full dataset is okay, app seems to use it for basic stats too)
    # The app code: patient_data = pd.read_csv('patient_dataset.csv')
    # It seems to expect one big file.
    full_dataset.to_csv('patient_dataset.csv', index=False)
    print("Created 'patient_dataset.csv'")

    # Save nft_metadata.csv
    # The app code: nft_metadata = pd.read_csv('nft_metadata.csv')
    # It merges on patient_id.
    # Columns needed: patient_id, wallet_id, allow_training, consent_timestamp, expiry_date, data_hash
    nft_columns = ['patient_id', 'wallet_id', 'allow_training', 'consent_timestamp', 'expiry_date', 'data_hash']
    
    # Check if columns exist
    missing_cols = [col for col in nft_columns if col not in full_dataset.columns]
    if missing_cols:
        print(f"Warning: Missing columns for NFT metadata: {missing_cols}")
    else:
        nft_metadata = full_dataset[nft_columns].copy()
        nft_metadata.to_csv('nft_metadata.csv', index=False)
        print("Created 'nft_metadata.csv'")

if __name__ == "__main__":
    regenerate_data()
