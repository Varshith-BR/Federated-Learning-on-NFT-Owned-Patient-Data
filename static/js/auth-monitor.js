/**
 * Auth Monitor - Checks for MetaMask account changes and clears session
 * Include this script in all portal pages
 */

async function checkAuthStatus() {
    if (typeof window.ethereum === 'undefined') {
        return;
    }

    try {
        // Get current MetaMask account
        const accounts = await ethereum.request({ method: 'eth_accounts' });

        if (accounts.length === 0) {
            // No account connected - redirect to login
            window.location.href = '/logout';
            return;
        }

        const currentAddress = accounts[0];

        // Check if this matches the server session
        const response = await fetch('/api/auth/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: currentAddress })
        });

        const data = await response.json();

        if (!data.valid || data.requires_reauth) {
            // Session invalid or address changed - redirect to login
            console.log('Auth mismatch detected, redirecting to login...');
            window.location.href = '/logout';
        }

    } catch (error) {
        console.error('Auth check error:', error);
    }
}

// Check auth on page load
window.addEventListener('load', () => {
    checkAuthStatus();
});

// Listen for MetaMask account changes
if (typeof window.ethereum !== 'undefined') {
    window.ethereum.on('accountsChanged', (accounts) => {
        console.log('MetaMask account changed');
        // Immediately redirect to logout to clear session
        window.location.href = '/logout';
    });

    window.ethereum.on('chainChanged', (chainId) => {
        window.location.href = '/logout';
    });
}

// Periodically check auth (every 10 seconds)
setInterval(checkAuthStatus, 10000);
