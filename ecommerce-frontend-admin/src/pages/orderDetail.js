import { getAllOrders, cancelOrder } from '../services/orderService.js';
import { findCustomerById } from '../services/customerService.js';
import { apiGet } from '../services/api.js';
import { config } from '../config/config.js';
import { showToast } from '../components/toast.js';
import { navigate } from '../core/router.js';

export const template = `
  <div class="max-w-5xl mx-auto">
    <div id="order-detail-content">
      <div class="flex items-center justify-center py-20">
        <div class="animate-spin w-8 h-8 border-2 border-red-500 border-t-transparent rounded-full"></div>
      </div>
    </div>
  </div>
`;

const STATUS_CONFIG = {
  PENDING:   { cls: 'bg-amber-500/10 text-amber-400 ring-1 ring-amber-500/30',       dot: 'bg-amber-500' },
  PAID:      { cls: 'bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/30', dot: 'bg-emerald-500' },
  CANCELLED: { cls: 'bg-red-500/10 text-red-400 ring-1 ring-red-500/30',             dot: 'bg-red-500' },
};

function statusBadge(status) {
  const cfg = STATUS_CONFIG[status] || { cls: 'bg-gray-700 text-gray-300', dot: 'bg-gray-400' };
  return `<span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-semibold ${cfg.cls}">
    <span class="w-2 h-2 rounded-full ${cfg.dot} flex-shrink-0"></span>${status}
  </span>`;
}

function formatDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}

async function getProductName(productUid) {
  try {
    const p = await apiGet(config.API.feed, `/products/${productUid}`);
    return p.name;
  } catch {
    return `Product ${productUid.slice(0, 8)}…`;
  }
}

export async function init({ id }) {
  const contentEl = document.getElementById('order-detail-content');
  if (!contentEl) return;

  let order;
  try {
    const allOrders = await getAllOrders();
    order = allOrders.find(o => o.id === id);
  } catch (err) {
    contentEl.innerHTML = `<div class="text-center py-20"><p class="text-red-400">${err.message}</p></div>`;
    return;
  }

  if (!order) {
    contentEl.innerHTML = `
      <div class="text-center py-20">
        <p class="text-gray-400 mb-4">Order not found.</p>
        <a href="#/orders" class="text-red-500 hover:underline text-sm font-medium">← Back to Orders</a>
      </div>`;
    return;
  }

  const [customer, enrichedItems] = await Promise.all([
    findCustomerById(order.userUid).catch(() => null),
    Promise.all(order.items.map(async item => ({
      ...item,
      name: await getProductName(item.productUid),
    }))),
  ]);

  const customerName = customer
    ? `${customer.firstName} ${customer.lastName}`.trim()
    : `User ${order.userUid.slice(0, 8)}…`;

  const subtotal = enrichedItems.reduce((s, i) => s + i.priceSnapshot * i.quantity, 0);
  const total = order.totalAmount || subtotal;

  function renderContent(currentOrder) {
    contentEl.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-2 mb-6">
        <a href="#/orders" class="flex items-center gap-2 text-gray-400 hover:text-red-500 transition-colors text-sm font-medium group">
          <svg class="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back to Orders
        </a>
        <div class="flex items-center gap-3">
          ${statusBadge(currentOrder.status)}
          ${currentOrder.status === 'PENDING' ? `
            <button id="cancel-btn"
              class="flex items-center gap-2 border border-red-500/40 text-red-400 hover:bg-red-500/10 px-4 py-2 rounded-xl text-sm font-semibold transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              Cancel Order
            </button>` : ''}
        </div>
      </div>

      <div class="bg-gray-800 rounded-2xl border border-gray-700 shadow-sm p-6 mb-5">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 class="text-xl font-bold text-white mb-1">Order #${currentOrder.id.slice(0, 8).toUpperCase()}</h1>
            <p class="text-gray-400 text-sm">${formatDate(currentOrder.createdAt)}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-gray-500 uppercase tracking-wide mb-1">Total Amount</p>
            <p class="text-2xl font-bold text-white">$${total.toFixed(2)}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div class="lg:col-span-2 bg-gray-800 rounded-2xl border border-gray-700 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-700">
            <h3 class="font-semibold text-white">Order Items</h3>
          </div>
          <!-- Mobile cards -->
          <div class="block md:hidden divide-y divide-gray-700/50">
            ${enrichedItems.map(item => `
              <div class="px-4 py-4">
                <div class="flex items-start justify-between gap-2 mb-2">
                  <div class="min-w-0">
                    <p class="font-semibold text-white text-sm">${item.name}</p>
                    <p class="text-xs text-gray-500 font-mono mt-0.5">${item.productUid.slice(0, 8)}…</p>
                  </div>
                  <span class="bg-gray-700 text-gray-200 font-semibold px-2 py-0.5 rounded-lg text-xs flex-shrink-0">×${item.quantity}</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-400">$${item.priceSnapshot.toFixed(2)} each</span>
                  <span class="font-bold text-white text-sm">$${(item.priceSnapshot * item.quantity).toFixed(2)}</span>
                </div>
              </div>`).join('')}
          </div>
          <!-- Desktop table -->
          <div class="hidden md:block overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-800/50 border-b border-gray-700">
                <tr>
                  <th class="text-left py-3 px-5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Product</th>
                  <th class="text-center py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Qty</th>
                  <th class="text-right py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Unit Price</th>
                  <th class="text-right py-3 px-5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                ${enrichedItems.map(item => `
                  <tr class="border-b border-gray-700/50">
                    <td class="py-4 px-5">
                      <p class="font-semibold text-white">${item.name}</p>
                      <p class="text-xs text-gray-500 font-mono mt-0.5">${item.productUid.slice(0, 8)}…</p>
                    </td>
                    <td class="py-4 px-4 text-center">
                      <span class="bg-gray-700 text-gray-200 font-semibold px-2.5 py-1 rounded-lg text-sm">×${item.quantity}</span>
                    </td>
                    <td class="py-4 px-4 text-right text-gray-400">$${item.priceSnapshot.toFixed(2)}</td>
                    <td class="py-4 px-5 text-right font-bold text-white">$${(item.priceSnapshot * item.quantity).toFixed(2)}</td>
                  </tr>`).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <div class="space-y-4">
          ${customer ? `
            <div class="bg-gray-800 rounded-2xl border border-gray-700 shadow-sm p-5">
              <h3 class="font-semibold text-white mb-4 text-sm">Customer</h3>
              <div class="flex items-center gap-3 mb-4">
                <div class="w-10 h-10 rounded-full bg-red-500 text-white flex items-center justify-center font-bold text-sm flex-shrink-0">
                  ${customerName.charAt(0).toUpperCase()}
                </div>
                <div>
                  <p class="font-semibold text-white text-sm">${customerName}</p>
                  <p class="text-xs text-gray-400">${customer.email}</p>
                </div>
              </div>
              <a href="#/customers/${customer.id}" class="flex items-center gap-1 text-xs text-red-500 hover:text-red-400 font-medium">
                View customer profile →
              </a>
            </div>` : `
            <div class="bg-gray-800 rounded-2xl border border-gray-700 shadow-sm p-5">
              <h3 class="font-semibold text-white mb-2 text-sm">Customer</h3>
              <p class="text-xs text-gray-500 font-mono">${order.userUid}</p>
            </div>`}

          <div class="bg-gray-800 rounded-2xl border border-gray-700 shadow-sm p-5">
            <h3 class="font-semibold text-white mb-4 text-sm">Order Summary</h3>
            <div class="space-y-2.5 text-sm">
              <div class="flex justify-between text-gray-400">
                <span>Items (${enrichedItems.length})</span>
                <span>$${subtotal.toFixed(2)}</span>
              </div>
              <div class="border-t border-gray-700 pt-2.5 flex justify-between font-bold text-white text-base">
                <span>Total</span>
                <span>$${total.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.getElementById('cancel-btn')?.addEventListener('click', async () => {
      const btn = document.getElementById('cancel-btn');
      btn.disabled = true;
      btn.textContent = 'Cancelling…';
      try {
        const updated = await cancelOrder(currentOrder.id);
        showToast('Order cancelled', 'success');
        renderContent(updated);
      } catch (err) {
        showToast(err.message, 'error');
        btn.disabled = false;
        btn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg> Cancel Order`;
      }
    });
  }

  renderContent(order);
}
