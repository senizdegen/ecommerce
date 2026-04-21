import { getOrderByUid } from '../services/orderService.js';
import { navigate } from '../core/router.js';

export const template = `
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 py-8">

      <!-- Step Indicator -->
      <div class="flex items-center justify-center gap-0 mb-10">
        <div class="flex items-center gap-1.5">
          <div class="w-7 h-7 rounded-full bg-gray-200 text-gray-400 flex items-center justify-center text-xs font-bold flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
          </div>
          <span class="text-xs font-medium text-gray-400 hidden sm:inline">Cart</span>
        </div>
        <div class="w-8 sm:w-12 h-px bg-gray-300 mx-2 sm:mx-3"></div>
        <div class="flex items-center gap-1.5">
          <div class="w-7 h-7 rounded-full bg-gray-200 text-gray-400 flex items-center justify-center text-xs font-bold flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
          </div>
          <span class="text-xs font-medium text-gray-400 hidden sm:inline">Checkout</span>
        </div>
        <div class="w-8 sm:w-12 h-px bg-red-300 mx-2 sm:mx-3"></div>
        <div class="flex items-center gap-1.5">
          <div class="w-7 h-7 rounded-full bg-red-500 text-white flex items-center justify-center text-xs font-bold flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
          </div>
          <span class="text-xs font-semibold text-gray-900">Confirmation</span>
        </div>
      </div>

      <div id="confirmation-content">
        <!-- loading skeleton -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 space-y-4">
          <div class="h-6 bg-gray-100 rounded-lg animate-pulse w-48 mx-auto"></div>
          <div class="h-4 bg-gray-100 rounded-lg animate-pulse w-64 mx-auto"></div>
          <div class="h-4 bg-gray-100 rounded-lg animate-pulse w-32 mx-auto"></div>
        </div>
      </div>

    </div>
  </div>
`;

export async function init(params = {}) {
  const content = document.getElementById('confirmation-content');
  const uid = params.uid || '';

  if (!uid) {
    content.innerHTML = `
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-10 text-center">
        <p class="text-gray-400 text-sm mb-4">Order not found.</p>
        <a href="#/orders" class="text-sm font-semibold text-red-500 hover:underline">View my orders</a>
      </div>`;
    return;
  }

  try {
    const data = await getOrderByUid(uid);

    if (!data) {
      content.innerHTML = `
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-10 text-center">
          <p class="text-gray-400 text-sm mb-4">Order not found.</p>
          <a href="#/orders" class="text-sm font-semibold text-red-500 hover:underline">View my orders</a>
        </div>`;
      return;
    }

    const order = data.order;
    const items = data.items || [];
    const displayId = order.uid ? order.uid.slice(0, 8) : '—';
    const date = order.createdAt ? order.createdAt.slice(0, 10) : '—';
    const total = typeof order.totalAmount === 'number' ? order.totalAmount : parseFloat(order.totalAmount ?? 0);
    const shipping = total > 50 ? 0 : 5.99;

    content.innerHTML = `
      <!-- Success Banner -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden mb-6">
        <div class="px-8 py-10 text-center">
          <div class="w-16 h-16 rounded-full bg-emerald-50 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 mb-2">Order Placed!</h1>
          <p class="text-gray-400 text-sm mb-4">Thank you for your purchase. We'll get it ready for you.</p>
          <div class="inline-flex items-center gap-2 bg-gray-50 rounded-xl px-4 py-2 border border-gray-100">
            <span class="text-xs text-gray-400 uppercase tracking-wide font-medium">Order</span>
            <span class="font-mono font-bold text-gray-800">#${displayId}</span>
            <span class="text-xs text-gray-400">${date}</span>
          </div>
        </div>
      </div>

      <!-- Items -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden mb-6">
        <div class="px-6 py-4 border-b border-gray-100">
          <h2 class="font-bold text-gray-900">Items Ordered</h2>
        </div>
        <div class="px-6 py-4">
          ${items.length > 0 ? `
            <div class="space-y-3">
              ${items.map(item => `
                <div class="flex items-center gap-3 py-2 border-b border-gray-50 last:border-0">
                  <div class="w-10 h-10 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center flex-shrink-0 overflow-hidden">
                    ${item.image
                      ? `<img src="${item.image}" alt="${item.name || ''}" class="w-full h-full object-contain p-1" />`
                      : `<svg class="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>`
                    }
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-700 truncate">${item.name || item.productUid}</p>
                    <p class="text-xs text-gray-400">Qty: ${item.quantity}</p>
                  </div>
                  <p class="text-sm font-semibold text-gray-800 flex-shrink-0">
                    $${(parseFloat(item.priceSnapshot) * item.quantity).toFixed(2)}
                  </p>
                </div>
              `).join('')}
            </div>
          ` : '<p class="text-sm text-gray-400">No item details available.</p>'}
        </div>
      </div>

      <!-- Summary -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-gray-100">
          <h2 class="font-bold text-gray-900">Order Summary</h2>
        </div>
        <div class="px-6 py-4 space-y-2.5 text-sm">
          <div class="flex justify-between text-gray-600">
            <span>Subtotal</span>
            <span class="font-medium text-gray-900">$${(total - shipping).toFixed(2)}</span>
          </div>
          <div class="flex justify-between text-gray-600">
            <span>Shipping</span>
            <span class="${shipping === 0 ? 'text-emerald-600 font-medium' : 'font-medium text-gray-900'}">
              ${shipping === 0 ? 'Free' : '$' + shipping.toFixed(2)}
            </span>
          </div>
          <div class="flex justify-between font-bold text-gray-900 border-t border-gray-100 pt-2.5 mt-1 text-base">
            <span>Total</span>
            <span>$${total.toFixed(2)}</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row gap-3">
        <a href="#/orders"
           class="flex-1 flex items-center justify-center gap-2 border-2 border-gray-200 text-gray-700 font-semibold py-3 rounded-xl hover:border-gray-300 transition-colors text-sm">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          View All Orders
        </a>
        <a href="#/products"
           class="flex-1 flex items-center justify-center gap-2 text-white font-semibold py-3 rounded-xl transition-all hover:-translate-y-0.5 text-sm"
           style="background:linear-gradient(135deg,#ef4444,#dc2626);box-shadow:0 4px 16px rgba(239,68,68,0.3);">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
          </svg>
          Continue Shopping
        </a>
      </div>
    `;
  } catch (err) {
    content.innerHTML = `
      <div class="bg-white rounded-2xl border border-red-100 shadow-sm p-8 text-center">
        <p class="text-red-500 text-sm font-medium mb-4">Failed to load order details.</p>
        <a href="#/orders" class="text-sm font-semibold text-gray-500 hover:text-gray-700">View my orders</a>
      </div>`;
  }
}