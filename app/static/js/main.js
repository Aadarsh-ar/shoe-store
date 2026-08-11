// ShoeStore Nike-Inspired Athletic E-Commerce JS

function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${type === 'danger' ? '✕' : '✓'} ${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// Global robust helper for Add to Cart API calls
async function addToCart(productId, size = "9", quantity = 1) {
  let targetSize = size;
  if (!targetSize || targetSize === 'undefined' || targetSize === 'null') {
    targetSize = "9";
  }

  try {
    const response = await fetch('/api/cart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_id: parseInt(productId),
        size: String(targetSize),
        quantity: parseInt(quantity)
      })
    });

    const data = await response.json();
    if (response.ok) {
      showToast(data.message || 'Added to Shopping Bag!', 'success');
      const badge = document.getElementById('cart-badge-count');
      if (badge && data.cart) {
        badge.innerText = data.cart.total_count;
        badge.style.display = data.cart.total_count > 0 ? 'flex' : 'none';
      }
    } else {
      showToast(data.error || 'Failed to add to bag', 'danger');
    }
  } catch (err) {
    console.error(err);
    showToast('Network error adding to bag.', 'danger');
  }
}

// Global helper for Wishlist toggle
async function toggleWishlist(productId, btnElement) {
  try {
    const isRemove = btnElement && btnElement.classList.contains('active');
    const response = await fetch('/api/wishlist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: parseInt(productId) })
    });

    const data = await response.json();
    if (response.ok) {
      if (btnElement) btnElement.classList.toggle('active');
      showToast(data.message || 'Wishlist Updated', 'success');
      const badge = document.getElementById('wishlist-badge-count');
      if (badge) {
        let cnt = parseInt(badge.innerText || '0');
        cnt = isRemove ? Math.max(0, cnt - 1) : cnt + 1;
        badge.innerText = cnt;
        badge.style.display = cnt > 0 ? 'flex' : 'none';
      }
    } else {
      if (response.status === 401) {
        showToast('Please sign in to save wishlist items.', 'warning');
        setTimeout(() => window.location.href = '/login', 1500);
      } else {
        showToast(data.error || 'Wishlist update failed', 'danger');
      }
    }
  } catch (err) {
    console.error(err);
    showToast('Error updating wishlist.', 'danger');
  }
}

// Carousel Scroll Navigation
function scrollCarousel(containerId, direction) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const scrollAmount = container.clientWidth * 0.75;
  container.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}

// Mobile Menu Drawer Toggle
function toggleMobileMenu() {
  const drawer = document.getElementById('mobile-drawer');
  if (drawer) drawer.classList.toggle('active');
}

// Search Overlay Toggle
function toggleSearchOverlay() {
  const overlay = document.getElementById('search-overlay');
  if (overlay) {
    const isVisible = overlay.style.display === 'flex';
    overlay.style.display = isVisible ? 'none' : 'flex';
    if (!isVisible) {
      const input = document.getElementById('search-overlay-input');
      if (input) input.focus();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const overlayInput = document.getElementById('search-overlay-input');
  if (overlayInput) {
    overlayInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        const val = overlayInput.value.trim();
        if (val) window.location.href = `/products?q=${encodeURIComponent(val)}`;
      }
    });
  }
});
