# Quick Test Script - Account Switching
# This helps verify that auth is working correctly

1. Open browser and navigate to http://localhost:5000
2. Open browser console (F12) to see [Auth] logs

## Test 1: Initial Login
- Should redirect to /login
- Import Admin account (index 0) in MetaMask
- Click "Connect MetaMask"
- Watch console logs:
  - Should see: [Auth] Current MetaMask address: 0x90f8...
  - Should see: [Auth] ✅ Auth validated
- Should redirect to /training (admin portal)

## Test 2: Switch Account Without Refresh
- In MetaMask, switch to Hospital account (index 2)
- Don't refresh yet
- Watch console logs:
  - Should see: [Auth] 🔄 MetaMask account changed detected!
  - Should automatically redirect to /logout then /login

## Test 3: Switch Account Then Refresh
- Login as Admin (index 0)
- Go to /training dashboard
- Switch MetaMask to Hospital (index 2)
- Now REFRESH the page (F5)
- Watch console logs:
  - Should see: [Auth] Current MetaMask address: 0x22d4...
  - Should see: [Auth] Saved session address: 0x90f8...
  - Should see: [Auth] ADDRESS MISMATCH! Clearing session and redirecting
  - Should redirect to /logout then /login

## Test 4: Login with Different Account
- Click "Connect MetaMask" at /login
- Should connect with current MetaMask account (Hospital - index 2)
- Watch console logs:
  - Should see: [Auth] ✅ Auth validated
- Should redirect to /hospital (hospital portal)
- Should ONLY see data from that hospital

## What to Check:
✅ Console shows correct address detection
✅ Mismatches trigger automatic redirect
✅ sessionStorage is cleared on account change
✅ Each account sees only their authorized data
✅ No errors in console

## Common Issues:
❌ If you see old account data: Clear browser cache, restart Flask
❌ If redirect loop: Check _auth_check_inline.html is included in base.html
❌ If no redirect on switch: Check MetaMask event listeners are working
