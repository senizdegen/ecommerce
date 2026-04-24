import { findCustomerById, deleteCustomer, updateCustomer } from '../services/customerService.js';
import { getAllOrders } from '../services/orderService.js';
import { showToast } from '../components/toast.js';
import { showModal } from '../components/modal.js';
import { navigate } from '../core/router.js';

export const template = `
  <div class="max-w-5xl mx-auto">
    <div id="customer-detail-content">
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
  return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${cfg.cls}">
    <span class="w-1.5 h-1.5 rounded-full ${cfg.dot} flex-shrink-0"></span>${status}
  </span>`;
}

function formatDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}

const AVATAR_COLORS = [
  'from-orange-500 to-violet-600',
  'from-emerald-400 to-teal-600',
  'from-amber-400 to-orange-500',
  'from-pink-500 to-rose-600',
  'from-cyan-400 to-blue-600',
];

export async function init({ id }) {
  const contentEl = document.getElementById('customer-detail-content');
  if (!contentEl) return;

  let customer;
  let allOrders = [];
  try {
    [customer, allOrders] = await Promise.all([
      findCustomerById(id),
      getAllOrders().catch(() => []),
    ]);
  } catch (err) {
    contentEl.innerHTML = `<div class="text-center py-20"><p class="text-red-400">${err.message}</p></div>`;
    return;
  }

  if (!customer) {
    contentEl.innerHTML = `
      <div class="text-center py-20">
        <p class="text-slate-500 mb-4">Customer not found.</p>
        <a href="#/customers" class="text-red-500 hover:underline text-sm font-medium">← Back to Customers</a>
      </div>`;
    return;
  }

  function render(c) {
    const customerOrders = allOrders
      .filter(o => String(o.userUid) === String(c.id))
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    const totalSpent = customerOrders.reduce((s, o) => s + (o.totalAmount || 0), 0);
    const avgOrder = customerOrders.length > 0 ? totalSpent / customerOrders.length : 0;
    const paidCount = customerOrders.filter(o => o.status === 'PAID').length;

    const fullName = `${c.firstName || ''} ${c.lastName || ''}`.trim();
    const initial = fullName.charAt(0).toUpperCase();
    const gradIdx = parseInt(id.replace(/\D/g, '')) % AVATAR_COLORS.length;
    const avatarGrad = AVATAR_COLORS[gradIdx];

    contentEl.innerHTML = `
      <div class="flex flex-wrap items-center justify-between gap-3 mb-6">
        <a href="#/customers" class="flex items-center gap-2 text-gray-400 hover:text-red-400 transition-colors text-sm font-medium group">
          <svg class="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back to Customers
        </a>
        <div class="flex items-center gap-2">
          <button id="edit-customer-btn"
            class="flex items-center gap-2 border border-gray-600 text-gray-300 hover:bg-gray-700 px-4 py-2 rounded-xl text-sm font-semibold transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            Edit
          </button>
          <button id="delete-customer-btn"
            class="flex items-center gap-2 border border-red-500/30 text-red-400 hover:bg-red-500/10 px-4 py-2 rounded-xl text-sm font-semibold transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            Delete
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-5">
        <div class="bg-gray-800 rounded-2xl border border-gray-700 p-6">
          <div class="flex flex-col items-center text-center">
            <div class="w-20 h-20 rounded-2xl bg-gradient-to-br ${avatarGrad} text-white flex items-center justify-center text-3xl font-bold mb-4 shadow-lg">
              ${initial}
            </div>
            <h2 class="text-xl font-bold text-white">${fullName}</h2>
            <p class="text-gray-400 text-sm mt-1">${c.email}</p>
            ${c.registeredDate ? `<p class="text-xs text-gray-500 mt-1">Joined ${c.registeredDate}</p>` : ''}
            ${c.isAdmin ? `<span class="mt-2 inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 ring-1 ring-red-500/30">Admin</span>` : ''}
          </div>

          <div class="border-t border-gray-700 mt-5 pt-5 space-y-3">
            <div class="flex items-start gap-3">
              <svg class="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <span class="text-sm text-gray-300">${c.email}</span>
            </div>
            <div class="flex items-start gap-3">
              <svg class="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"/>
              </svg>
              <span class="text-sm font-mono text-gray-500">ID: ${c.id}</span>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 grid grid-cols-2 gap-3">
          ${[
            { label: 'Total Orders', value: customerOrders.length, icon: 'bg-red-500/10 text-red-400', svg: `<svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>` },
            { label: 'Total Spent', value: `$${totalSpent.toFixed(2)}`, icon: 'bg-emerald-500/10 text-emerald-400', svg: `<svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>` },
            { label: 'Avg Order', value: `$${avgOrder.toFixed(2)}`, icon: 'bg-violet-500/10 text-violet-400', svg: `<svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>` },
            { label: 'Paid Orders', value: paidCount, icon: 'bg-amber-500/10 text-amber-400', svg: `<svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>` },
          ].map(s => `
            <div class="bg-gray-800 rounded-2xl border border-gray-700 p-3 sm:p-5 flex items-center gap-2 sm:gap-4 min-w-0">
              <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl ${s.icon} flex items-center justify-center flex-shrink-0">${s.svg}</div>
              <div class="min-w-0">
                <p class="text-base sm:text-xl font-bold text-white leading-tight truncate">${s.value}</p>
                <p class="text-xs text-gray-500 truncate">${s.label}</p>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-700 flex items-center justify-between">
          <h3 class="font-semibold text-white">Order History</h3>
          <span class="text-sm text-gray-500">${customerOrders.length} order${customerOrders.length !== 1 ? 's' : ''}</span>
        </div>
        ${customerOrders.length === 0
          ? `<div class="p-12 text-center text-gray-500 text-sm">No orders yet.</div>`
          : `<div class="block md:hidden divide-y divide-gray-700/50">
              ${customerOrders.map(o => `
                <div class="px-4 py-4 flex items-center justify-between gap-3 cursor-pointer hover:bg-gray-700/40 transition-colors" onclick="window.location.hash='#/orders/${o.uid}'">
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 flex-wrap mb-1">
                      <span class="font-mono text-xs font-semibold text-red-500 bg-red-500/10 px-2 py-0.5 rounded-md">#${o.uid.slice(0, 8).toUpperCase()}</span>
                      ${statusBadge(o.status)}
                    </div>
                    <p class="text-xs text-gray-400">
                      <span class="font-semibold text-white">$${(o.totalAmount || 0).toFixed(2)}</span>
                      <span class="mx-1 text-gray-600">·</span>
                      ${formatDate(o.createdAt)}
                    </p>
                  </div>
                  <svg class="w-4 h-4 text-gray-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </div>
              `).join('')}
            </div>
            <div class="hidden md:block overflow-x-auto">
              <table class="w-full text-sm">
                <thead class="bg-gray-800/50 border-b border-gray-700">
                  <tr>
                    <th class="text-left py-3 px-5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Order ID</th>
                    <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Total</th>
                    <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Status</th>
                    <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Date</th>
                  </tr>
                </thead>
                <tbody>
                  ${customerOrders.map(o => `
                    <tr class="border-b border-gray-700/50 hover:bg-gray-700/50 transition-colors">
                      <td class="py-3.5 px-5">
                        <span class="font-mono text-xs font-semibold text-red-500 bg-red-500/10 px-2.5 py-1 rounded-lg">#${o.uid.slice(0, 8).toUpperCase()}</span>
                      </td>
                      <td class="py-3.5 px-4 font-bold text-white">$${(o.totalAmount || 0).toFixed(2)}</td>
                      <td class="py-3.5 px-4">${statusBadge(o.status)}</td>
                      <td class="py-3.5 px-4 text-gray-500 text-xs">${formatDate(o.createdAt)}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>`
        }
      </div>
    `;

    // Edit button
    document.getElementById('edit-customer-btn').addEventListener('click', () => {
      showEditModal(c);
    });

    // Delete button
    document.getElementById('delete-customer-btn').addEventListener('click', () => {
      showModal({
        title: 'Delete Customer',
        body: `Are you sure you want to delete <strong>${fullName}</strong>? This cannot be undone.`,
        onConfirm: async () => {
          try {
            await deleteCustomer(c.id);
            showToast('Customer deleted', 'success');
            navigate('/customers');
          } catch (err) {
            showToast(err.message, 'error');
          }
        }
      });
    });
  }

  function showEditModal(c) {
    // Создаём модалку редактирования инлайн
    const existing = document.getElementById('edit-modal-overlay');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.id = 'edit-modal-overlay';
    overlay.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4';
    overlay.innerHTML = `
      <div class="bg-gray-800 rounded-2xl border border-gray-700 shadow-2xl w-full max-w-md p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-white">Edit Customer</h3>
          <button id="edit-modal-close" class="text-gray-500 hover:text-white transition-colors p-1">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">First Name</label>
            <input id="edit-first-name" type="text" value="${c.firstName || ''}"
              class="w-full px-3 py-2.5 bg-gray-700 border border-gray-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">Last Name</label>
            <input id="edit-last-name" type="text" value="${c.lastName || ''}"
              class="w-full px-3 py-2.5 bg-gray-700 border border-gray-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">Email</label>
            <input id="edit-email" type="email" value="${c.email || ''}"
              class="w-full px-3 py-2.5 bg-gray-700 border border-gray-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all" />
          </div>
          <div class="flex items-center gap-3 py-1">
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" id="edit-is-admin" ${c.isAdmin ? 'checked' : ''} class="sr-only peer" />
              <div class="w-10 h-5 bg-gray-600 peer-focus:ring-2 peer-focus:ring-red-500 rounded-full peer peer-checked:bg-red-500 transition-colors"></div>
              <div class="absolute left-0.5 top-0.5 w-4 h-4 bg-white rounded-full transition-transform peer-checked:translate-x-5"></div>
            </label>
            <span class="text-sm text-gray-300">Admin access</span>
          </div>
        </div>

        <div id="edit-error" class="hidden mt-3 text-sm text-red-400"></div>

        <div class="flex gap-3 mt-6">
          <button id="edit-cancel-btn"
            class="flex-1 py-2.5 border border-gray-600 text-gray-300 rounded-xl text-sm font-semibold hover:bg-gray-700 transition-colors">
            Cancel
          </button>
          <button id="edit-save-btn"
            class="flex-1 py-2.5 bg-red-500 hover:bg-red-600 text-white rounded-xl text-sm font-semibold transition-colors flex items-center justify-center gap-2">
            Save Changes
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    const close = () => overlay.remove();

    document.getElementById('edit-modal-close').addEventListener('click', close);
    document.getElementById('edit-cancel-btn').addEventListener('click', close);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

    document.getElementById('edit-save-btn').addEventListener('click', async () => {
      const saveBtn = document.getElementById('edit-save-btn');
      const errorEl = document.getElementById('edit-error');

      const firstName = document.getElementById('edit-first-name').value.trim();
      const lastName = document.getElementById('edit-last-name').value.trim();
      const email = document.getElementById('edit-email').value.trim();
      const isAdmin = document.getElementById('edit-is-admin').checked;

      if (!firstName || !lastName || !email) {
        errorEl.textContent = 'All fields are required.';
        errorEl.classList.remove('hidden');
        return;
      }

      saveBtn.disabled = true;
      saveBtn.innerHTML = `
        <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        Saving...`;

      try {
        const updated = await updateCustomer(c.id, {
          first_name: firstName,
          last_name: lastName,
          email,
          is_admin: isAdmin,
        });
        customer = updated;
        close();
        showToast('Customer updated successfully', 'success');
        render(updated);
      } catch (err) {
        errorEl.textContent = err.message || 'Failed to update customer.';
        errorEl.classList.remove('hidden');
        saveBtn.disabled = false;
        saveBtn.innerHTML = 'Save Changes';
      }
    });
  }

  render(customer);
}