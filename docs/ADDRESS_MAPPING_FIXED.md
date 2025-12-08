# ⚠️ IMPORTANT: Address Mappings Updated!

## What Changed

The address mappings have been updated to use the **actual addresses** from your running Ganache instance instead of hardcoded addresses.

## Account Index Reference

Here's which Ganache account index corresponds to which role:

### Admins
- **Index 0**: Admin 1 (FL System Administrator)
- **Index 1**: Admin 2 (Research Coordinator)

### Hospitals
- **Index 2**: Metro General Hospital
- **Index 3**: Regional Healthcare System
- **Index 4**: St. Mary's Hospital
- **Index 5**: University Medical Center
- **Index 6**: Community Health Network
- **Index 7**: City Medical Center
- **Index 8**: Veterans Affairs Hospital
- **Index 9**: Children's Medical Center

### Patients
- **Index 10-19**: Patient accounts (P000023, P000028, etc.)

## How to Use MetaMask

### Option 1: Import by Account Index (Easiest!)
In MetaMask, when adding an account from Ganache:
1. Click "Import Account"
2. Select "Select Type" → Choose "Private Key"
3. In Ganache GUI or terminal, find account by index (0-19)
4. Copy the private key for that index
5. Paste in MetaMask

### Option 2: Check address_mapping.csv
1. Open `address_mapping.csv`
2. Find the address for the role you want to test
3. Match that address in Ganache to get the private key
4. Import the private key in MetaMask

## Testing

### Test as Admin (Use Index 0 or 1)
```
1. Import private key from Ganache account index 0 or 1
2. Connect wallet at /login
3. Should redirect to /training
4. Full access granted
```

### Test as Hospital (Use Index 2-9)
```
1. Import private key from Ganache account index 2-9
   Example: Index 2 = Metro General Hospital
2. Connect wallet
3. Should redirect to /hospital
4. Only see patients from that hospital
```

### Test as Patient (Use Index 10-19)
```
1. Import private key from Ganache account index 10-19
2. Connect wallet
3. Should redirect to /patient
4. Only see your own medical record
```

## ⚡ RESTART REQUIRED

**Important:** You must restart the Flask app for the new mappings to take effect!

```bash
# Press Ctrl+C in the terminal running Flask
# Then restart:
python app.py
```

The app loads `address_mapping.csv` on startup, so changes won't apply until you restart.

## Verification

To verify the mappings are correct:
1. Check `address_mapping.csv` - it should have addresses matching your Ganache
2. In Ganache, compare the first address with the first line in the CSV
3. They should match (case-insensitive)
