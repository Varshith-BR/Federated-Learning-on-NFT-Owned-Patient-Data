# 🌐 Application URLs - Quick Reference

## Main Access URL
**Start Here:** `http://localhost:5000`

This will automatically redirect you to `/login` if not authenticated.

---

## 🔐 Authentication Flow

### 1. Login Page
**URL:** `http://localhost:5000/login`

- Connect your MetaMask wallet
- System detects your role automatically
- Redirects to appropriate portal

### 2. Logout
**URL:** `http://localhost:5000/logout`

- Clears session
- Redirects back to login

---

## 📍 Role-Based Portal URLs

### Admin Portals (Account Index 0-1)
After logging in as Admin, you'll be redirected to:

**FL Training Dashboard:** `http://localhost:5000/training`
- Start federated learning training
- Monitor training progress
- View all hospital nodes
- Access full analytics

**Alternative Admin URLs:**
- Main Dashboard: `http://localhost:5000/dashboard`
- Blockchain Explorer: `http://localhost:5000/blockchain`

### Hospital Portals (Account Index 2-9)
After logging in as Hospital, you'll be redirected to:

**Hospital Portal:** `http://localhost:5000/hospital`
- View YOUR hospital's patients only
- See consent statistics
- Analytics for your institution

### Patient Portals (Account Index 10-19)
After logging in as Patient, you'll be redirected to:

**Patient Portal:** `http://localhost:5000/patient`
- View YOUR medical records only
- Manage YOUR consent status
- See YOUR NFT information

---

## 🔗 Direct Portal Access

You can try to access portals directly, but:
- ❌ **Without authentication** → Redirects to `/login`
- ❌ **Wrong role** → Returns 403 Forbidden error
- ✅ **Correct role** → Shows portal

**Examples:**
```
http://localhost:5000/training   → Admin only
http://localhost:5000/hospital   → Hospital only
http://localhost:5000/patient    → Patient only
```

---

## 🌍 Network Access

### Local Access (Same Computer)
```
http://localhost:5000
http://127.0.0.1:5000
```

### Mobile/LAN Access (Other Devices)
Check Flask startup output for your local IP:
```
http://192.168.x.x:5000
```

Replace `192.168.x.x` with the IP shown in terminal when Flask starts.

---

## 🧪 Testing Different Roles

### Quick Test Flow:

1. **Open:** `http://localhost:5000`
2. **Login as Admin** (MetaMask account index 0)
   - Should redirect to: `http://localhost:5000/training`
   - Can see all hospitals and data

3. **Switch MetaMask** to Hospital (index 2)
   - Should auto-redirect to `/logout`
   - Login again
   - Should redirect to: `http://localhost:5000/hospital`
   - Can only see Metro General Hospital data

4. **Switch MetaMask** to Patient (index 10)
   - Should auto-redirect to `/logout`
   - Login again
   - Should redirect to: `http://localhost:5000/patient`
   - Can only see your own patient record

---

## 📊 API Endpoints (For Reference)

These are used by the frontend, but you can test them:

### Authentication
- `POST /api/auth/verify` - Verify wallet address
- `POST /api/auth/check` - Check current session

### Data Access (Filtered by Role)
- `GET /api/patients` - Get patient data (filtered)
- `GET /api/nodes` - Get hospital nodes (filtered)
- `GET /api/blockchain` - Get blockchain data
- `GET /api/training_history` - Get FL training history

### Training (Admin Only)
- `POST /api/start_training` - Start FL training
- `GET /api/training_status` - Get training status

---

## ⚠️ Common Issues

### "Stuck on old account"
**Solution:** 
- Clear browser cache (Ctrl+Shift+Delete)
- Or use Incognito/Private window
- Restart Flask app

### "Cannot access portal"
**Solution:**
- Check you're using the correct MetaMask account
- Verify account is imported from Ganache
- Check browser console (F12) for errors

### "Redirect loop"
**Solution:**
- Ensure Ganache is running on port 7545
- Restart Flask app
- Clear browser cache

---

## ✅ Recommended Workflow

1. Start Ganache: `ganache --accounts 20 --port 7545 --deterministic`
2. Start Flask: `python app.py`
3. Open browser to: `http://localhost:5000`
4. Import MetaMask account for desired role
5. Connect wallet at login page
6. Access appropriate portal automatically

**That's it!** The system handles authentication and routing automatically.
