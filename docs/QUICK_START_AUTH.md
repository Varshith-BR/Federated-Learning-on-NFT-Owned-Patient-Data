# 🚀 Quick Start Guide: Ganache Address-Based Authentication (30 Accounts)

## Prerequisites
```bash
# Install Ganache
npm install -g ganache

# Install MetaMask browser extension
# https://metamask.io/download/
```

## Step 1: Start Ganache with 30 Accounts
```bash
# IMPORTANT: Use --accounts 30 and --deterministic flags
ganache --accounts 30 --port 7545 --networkId 1337 --deterministic
```

Keep this terminal running!

## Step 2: Generate Address Mappings
```bash
python generate_address_mappings.py
```

This will create `address_mapping.csv` with **30 mapped accounts**:
- **Accounts 0-1**: 2 Admins (full access)
- **Accounts 2-9**: 8 Hospitals (filtered data access)
- **Accounts 10-29**: 20 Patients (own records only)

## Step 3: Configure MetaMask

### Add Localhost Network
1. Open MetaMask
2. Click network dropdown → "Add Network"
3. **Manual Network Settings**:
   - Network Name: `Ganache Local`
   - RPC URL: `http://127.0.0.1:7545`
   - Chain ID: `1337`
   - Currency Symbol: `ETH`

### Import Test Accounts
Use private keys from Ganache (shown in terminal when started with `--deterministic`)

#### Admin Account (Index 0)
```
Private Key: 0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
Address: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1
Role: Admin - Full FL Training Access
```

#### Hospital Account (Index 2 - Metro General)
```
Private Key: 0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1
Address: 0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b
Role: Hospital - View Metro General patients only
```

#### Patient Account (Index 10)
```
Private Key: 0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c
Address: 0x610Bb1573d1046FCb8A70Bbbd395754cD57C2b60
Role: Patient - View own medical records only
```

**Note**: With 30 accounts, you now have 20 patient accounts (index 10-29) for more comprehensive testing!

### Importing in MetaMask
1. Click account icon (top right)
2. Select "Import Account"
3. Paste private key
4. Import
5. Repeat for each role you want to test

## Step 4: Start Flask Application
```bash
cd "c:\Users\91861\Desktop\major project\FL_goodUI"
python app.py
```

## Step 5: Access Application
1. Open browser to `http://localhost:5000`
2. You'll be redirected to `/login`
3. Click "Connect MetaMask"
4. MetaMask will prompt for connection - **Approve**
5. You'll be redirected based on your role:
   - **Admin** → `/training` (FL Training Dashboard)
   - **Hospital** → `/hospital` (Hospital Portal with filtered data)
   - **Patient** → `/patient` (Patient Portal with your records)

## Testing Different Roles

### Test as Admin
1. Switch to Admin account in MetaMask (index 0 or 1)
2. Refresh page or logout and reconnect
3. ✅ Should see full FL Training Dashboard
4. ✅ Can start training rounds
5. ✅ Can view all hospitals and analytics

### Test as Hospital
1. Switch to Hospital account in MetaMask (index 2-9)
2. Refresh page or logout and reconnect
3. ✅ Should see Hospital Portal
4. ✅ Only see patients from your hospital
5. ✅ Cannot access training dashboard
6. ✅ Cannot see other hospitals' data

### Test as Patient
1. Switch to Patient account in MetaMask (index 10-29)
2. Refresh page or reconnect
3. ✅ Should see Patient Portal
4. ✅ Only see YOUR medical records
5. ✅ Can update YOUR consent status
6. ✅ Cannot see other patients' data

## Account Index Reference

| Index Range | Role | Count | Access Level |
|-------------|------|-------|--------------|
| 0-1 | Admin | 2 | Full system access |
| 2-9 | Hospital | 8 | Hospital-specific data |
| 10-29 | Patient | 20 | Own records only |

**Total: 30 accounts**

## Troubleshooting

### Issue: "Wrong Network"
**Solution**: Switch MetaMask network to "Ganache Local" (localhost:7545)

### Issue: "Address not recognized"
**Solution**: 
- Ensure you started Ganache with `--accounts 30 --deterministic`
- Check you imported the correct private key
- Verify address mapping file exists: `address_mapping.csv`
- Run `python generate_address_mappings.py` again

### Issue: "Cannot connect wallet"
**Solution**:
- Ensure Ganache is running on port 7545
- Check MetaMask is unlocked
- Try disconnecting and reconnecting in MetaMask

### Issue: "Unauthorized access"
**Solution**: You're trying to access a portal you don't have permission for. Use the role-appropriate account.

## Security Notes
⚠️ **THESE ARE TEST ACCOUNTS ONLY**
- Never use these private keys on mainnet
- Never send real ETH to these addresses
- This is for local testing only with Ganache

## Quick Reference

| Role | Default Redirect | Can Access |
|------|-----------------|-----------|
| Admin | `/training` | All portals, all data |
| Hospital | `/hospital` | Only their hospital's data |
| Patient | `/patient` | Only their own records |

**New**: With 30 accounts, you can now test with 20 different patient accounts for more comprehensive role-based access testing!
