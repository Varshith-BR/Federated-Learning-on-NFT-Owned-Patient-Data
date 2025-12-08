# Ganache Address-Based Authentication Guide

## 🔐 Overview
This system uses Ethereum addresses from Ganache to authenticate users and control access.

## 📋 Address Assignments

### 🔧 Admin Accounts (Full Access)

**FL System Administrator**
- Address: `0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1`
- Entity ID: `admin_001`
- Access: Full access to all portals and training controls

**Research Coordinator**
- Address: `0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0`
- Entity ID: `admin_002`
- Access: Full access to FL training and analytics

### 🏥 Hospital Accounts

**Metro General Hospital**
- Address: `0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b`
- Node ID: `node_metro_general`
- Access: View only patients from this hospital

**Regional Healthcare System**
- Address: `0xE11BA2b4D45Eaed5996Cd0823791E0C93114882d`
- Node ID: `node_regional`
- Access: View only patients from this hospital

**St. Mary's Hospital**
- Address: `0xd03ea8624C8C5987235048901fB614fDcA89b117`
- Node ID: `node_st_marys`
- Access: View only patients from this hospital

**University Medical Center**
- Address: `0x95cED938F7991cd0dFcb48F0a06a40FA1aF46EBC`
- Node ID: `node_university`
- Access: View only patients from this hospital

**Community Health Network**
- Address: `0x3E5e9111Ae8eB78Fe1CC3bb8915d5D461F3Ef9A9`
- Node ID: `node_community`
- Access: View only patients from this hospital

**City Medical Center**
- Address: `0x28a8746e75304c0780E011BEd21C72cD78cd535E`
- Node ID: `node_city`
- Access: View only patients from this hospital

**Veterans Affairs Hospital**
- Address: `0xACa94ef8bD5ffEE41947b4585a84BdA5a3d3DA6E`
- Node ID: `node_veterans`
- Access: View only patients from this hospital

**Children's Medical Center**
- Address: `0x1dF62f291b2E969fB0849d99D9Ce41e2F137006e`
- Node ID: `node_childrens`
- Access: View only patients from this hospital

### 👤 Patient Accounts

**Patient P000023**
- Address: `0x610Bb1573d1046FCb8A70Bbbd395754cD57C2b60`
- Patient ID: `P000023`
- Access: View only personal medical records

**Patient P000028**
- Address: `0x855FA758c77D68a04990E992aA4dcdeF899F654A`
- Patient ID: `P000028`
- Access: View only personal medical records

**Patient P000034**
- Address: `0xfA2435Eacf10Ca62ae6787ba2fB044f8733Ee843`
- Patient ID: `P000034`
- Access: View only personal medical records

**Patient P000055**
- Address: `0x64E078A8Aa15A41B85890265648e965De686bAE6`
- Patient ID: `P000055`
- Access: View only personal medical records

**Patient P000064**
- Address: `0x2F560290FEF1B3Ada194b6aA9c40aa71f8e95598`
- Patient ID: `P000064`
- Access: View only personal medical records

**Patient P000077**
- Address: `0xf408f04F9b7691f7174FA2bb73ad6d45fD5d3CBe`
- Patient ID: `P000077`
- Access: View only personal medical records

**Patient P000087**
- Address: `0x66FC63C2572bF3ADD0FE5d44b97c2E614E35e9a3`
- Patient ID: `P000087`
- Access: View only personal medical records

**Patient P000096**
- Address: `0xF0D5BC18421fa04D0a2A2ef540ba5A9f04014BE3`
- Patient ID: `P000096`
- Access: View only personal medical records

**Patient P000100**
- Address: `0x92c853c283a2E4668C0D5e0eD0e24978084215d1`
- Patient ID: `P000100`
- Access: View only personal medical records

**Patient P000145**
- Address: `0x4Fc5BC18421fa04D0a2A2ef540ba5A9f04014BE4`
- Patient ID: `P000145`
- Access: View only personal medical records


## 🚀 How to Use

### Step 1: Start Ganache
```bash
# Install Ganache globally
npm install -g ganache

# Start Ganache with these exact accounts
ganache --accounts 20 --port 7545 --networkId 1337 --deterministic
```

**IMPORTANT**: Use `--deterministic` flag to ensure the same addresses are generated every time!

### Step 2: Install MetaMask
1. Install MetaMask browser extension
2. Click on MetaMask icon
3. Select "Import using Secret Recovery Phrase"
4. Or click "Import Account" and paste private key

### Step 3: Import Ganache Accounts
For each role you want to test:

1. Open Ganache GUI or terminal
2. Copy the private key for the desired account
3. In MetaMask: Click account icon → Import Account → Paste private key

**Example Private Keys** (from Ganache deterministic seed):
```
Admin 1: 0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
Hospital (Metro General): 0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1
Patient 1: 0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c
```

### Step 4: Connect to Application
1. Navigate to the login page
2. Click "Connect Wallet"
3. MetaMask will prompt for approval
4. Your role will be detected automatically
5. You'll be redirected to the appropriate portal:
   - **Admin** → FL Training Dashboard
   - **Hospital** → Hospital Portal with filtered data
   - **Patient** → Patient Portal with your records only

## 🧪 Testing Different Roles

### Test as Admin
```
1. Import Admin address in MetaMask
2. Connect wallet
3. You should see full FL Training Dashboard
4. Can start training, view all hospitals, see all analytics
```

### Test as Hospital
```
1. Import any hospital address (e.g., Metro General)
2. Connect wallet
3. You should see Hospital Dashboard
4. Only patients from YOUR hospital visible
5. Can view analytics for your institution only
```

### Test as Patient
```
1. Import a patient address
2. Connect wallet
3. You should see Patient Portal
4. Only YOUR medical records visible
5. Can manage consent for your data
```

## 🔍 Troubleshooting

**Problem**: MetaMask shows wrong network
- **Solution**: Change MetaMask network to Localhost 7545

**Problem**: Address not recognized
- **Solution**: Ensure you imported the correct private key from the list above

**Problem**: Ganache addresses changed
- **Solution**: Always start Ganache with `--deterministic` flag

## 📊 Quick Reference Table

| Role | Address (First 10 chars) | Access Level |
|------|-------------------------|--------------|
| Admin | `0x90F8bf6A...` | FL System Administrator |
| Admin | `0xFFcf8FDE...` | Research Coordinator |
| Hospital | `0x22d491Bd...` | Metro General Hospital |
| Hospital | `0xE11BA2b4...` | Regional Healthcare System |
| Hospital | `0xd03ea862...` | St. Mary's Hospital |
| Hospital | `0x95cED938...` | University Medical Center |
| Hospital | `0x3E5e9111...` | Community Health Network |
| Hospital | `0x28a8746e...` | City Medical Center |
| Hospital | `0xACa94ef8...` | Veterans Affairs Hospital |
| Hospital | `0x1dF62f29...` | Children's Medical Center |
| Patient | `0x610Bb157...` | Patient P000023 |
| Patient | `0x855FA758...` | Patient P000028 |
| Patient | `0xfA2435Ea...` | Patient P000034 |
| Patient | `0x64E078A8...` | Patient P000055 |
| Patient | `0x2F560290...` | Patient P000064 |
| Patient | `0xf408f04F...` | Patient P000077 |
| Patient | `0x66FC63C2...` | Patient P000087 |
| Patient | `0xF0D5BC18...` | Patient P000096 |
| Patient | `0x92c853c2...` | Patient P000100 |
| Patient | `0x4Fc5BC18...` | Patient P000145 |

## 🔗 Next Steps

1. Start Ganache with deterministic flag
2. Import at least one address per role in MetaMask
3. Test authentication flow
4. Verify data filtering works correctly
5. Test consent updates from patient account
