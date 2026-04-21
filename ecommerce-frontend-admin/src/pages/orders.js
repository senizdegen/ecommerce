import { getAllOrders } from '../services/orderService.js';
import { findAllCustomers } from '../services/customerService.js';
import { navigate } from '../core/router.js';

const STATUSES = ['PENDING', 'PAID', 'CANCELLED'];

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

export const template = `
  <div class="max-w-7xl mx-auto">
    <div class="flex flex-wrap items-center justify-between gap-y-2 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-white">Orders</h1>
        <p id="orders-count" class="text-sm text-gray-400 mt-0.5"></p>
      </div>
    </div>

    <div class="bg-gray-800 rounded-2xl border border-gray-700 p-4 mb-5 flex flex-wrap gap-3 shadow-sm">
      <div class="relative flex-1 min-w-0">
        <svg class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0"/>
        </svg>
        <input id="search-input" type="text" placeholder="Search order ID or customer..."
          class="w-full pl-9 pr-3 py-2 border border-gray-600 rounded-xl text-sm bg-gray-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all" />
      </div>
      <select id="status-filter"
        class="w-full sm:w-auto border border-gray-600 rounded-xl px-3 py-2 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all bg-gray-700">
        <option value="">All Statuses</option>
        ${STATUSES.map(s => `<option value="${s}">${s}</option>`).join('')}
      </select>
    </div>

    <div id="status-summary" class="grid grid-cols-3 gap-3 mb-5"></div>

    <div class="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden shadow-sm">
      <div id="orders-table"></div>
      <div id="pagination" class="flex flex-wrap items-center justify-between gap-2 px-4 py-3 border-t border-gray-700"></div>
    </div>
  </div>
`;

export async function init() {
  const PAGE_SIZE = 10;
  let allOrders = [];
  let allCustomers = [];

  try {
    [allOrders, allCustomers] = await Promise.all([
      getAllOrders(),
      findAllCustomers().catch(() => []),
    ]);
  } catch (err) {
    document.getElementById('orders-table').innerHTML = `
      <div class="p-16 text-center">
        <p class="text-red-400 font-medium">Failed to load orders</p>
        <p class="text-gray-500 text-sm mt-1">${err.message}</p>
      </div>`;
    return;
  }

  let statusFilter = '';
  let searchQuery = '';
  let currentPage = 1;

  function getUserName(userUid) {
    const c = allCustomers.find(c => String(c.id) === String(userUid));
    return c ? `${c.firstName} ${c.lastName}`.trim() : String(userUid).slice(0, 8) + '…';
  }

  function getFiltered() {
    return allOrders
      .filter(o => !statusFilter || o.status === statusFilter)
      .filter(o => {
        if (!searchQuery) return true;
        const q = searchQuery.toLowerCase();
        return o.id.toLowerCase().includes(q) || getUserName(o.userUid).toLowerCase().includes(q);
      });
  }

  function renderStatusSummary() {
    const summaryEl = document.getElementById('status-summary');
    if (!summaryEl) return;
    const cfg = STATUS_CONFIG;
    summaryEl.innerHTML = STATUSES.map(s => {
      const count = allOrders.filter(o => o.status === s).length;
      return `
        <div class="bg-gray-800 rounded-xl border border-gray-700 px-3 py-3 flex items-center gap-2 shadow-sm cursor-pointer hover:border-red-500 transition-colors ${statusFilter === s ? 'border-red-500 ring-2 ring-red-900/40' : ''}"
             data-status-quick="${s}">
          <span class="w-2 h-2 rounded-full ${cfg[s]?.dot || 'bg-gray-400'} flex-shrink-0"></span>
          <div class="min-w-0">
            <p class="text-base font-bold text-white leading-tight">${count}</p>
            <p class="text-xs text-gray-400 truncate">${s}</p>
          </div>
        </div>`;
    }).join('');

    summaryEl.querySelectorAll('[data-status-quick]').forEach(el => {
      el.addEventListener('click', () => {
        const s = el.dataset.statusQuick;
        statusFilter = statusFilter === s ? '' : s;
        document.getElementById('status-filter').value = statusFilter;
        currentPage = 1;
        renderStatusSummary();
        renderTable();
      });
    });
  }

  function renderTable() {
    const filtered = getFiltered();
    const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    if (currentPage > totalPages) currentPage = totalPages;
    const paginated = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);

    const countEl = document.getElementById('orders-count');
    if (countEl) countEl.textContent = `${allOrders.length} order${allOrders.length !== 1 ? 's' : ''}`;

    const tableEl = document.getElementById('orders-table');
    if (!tableEl) return;

    if (paginated.length === 0) {
      tableEl.innerHTML = `
        <div class="p-16 text-center">
          <svg class="w-10 h-10 text-gray-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <p class="text-gray-400 font-medium">No orders found</p>
        </div>`;
    } else {
      tableEl.innerHTML = `
        <!-- Mobile cards -->
        <div class="block md:hidden divide-y divide-gray-700/50">
          ${paginated.map(o => `
            <div class="px-4 py-4 flex items-start justify-between gap-3 cursor-pointer hover:bg-gray-700/40 active:bg-gray-700/60 transition-colors" data-order-id="${o.id}">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap mb-1.5">
                  <span class="font-mono text-xs font-semibold text-red-500 bg-red-500/10 px-2 py-0.5 rounded-md">#${o.id.slice(0, 8).toUpperCase()}</span>
                  ${statusBadge(o.status)}
                </div>
                <p class="font-semibold text-white text-sm truncate">${getUserName(o.userUid)}</p>
                <p class="text-xs text-gray-400 mt-0.5">
                  <span class="font-semibold text-white">$${o.totalAmount.toFixed(2)}</span>
                  <span class="mx-1 text-gray-600">·</span>${o.items.length} item${o.items.length !== 1 ? 's' : ''}
                  <span class="mx-1 text-gray-600">·</span>${formatDate(o.createdAt)}
                </p>
              </div>
              <svg class="w-4 h-4 text-gray-600 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </div>`).join('')}
        </div>
        <!-- Desktop table -->
        <div class="hidden md:block overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-800/50 border-b border-gray-700">
              <tr>
                <th class="text-left py-3 px-5 text-xs font-semibold text-gray-400 uppercase tracking-wide">Order ID</th>
                <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Customer</th>
                <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Items</th>
                <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Total</th>
                <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Status</th>
                <th class="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase tracking-wide">Date</th>
                <th class="py-3 px-4"></th>
              </tr>
            </thead>
            <tbody>
              ${paginated.map(o => `
                <tr class="border-b border-gray-700/50 hover:bg-gray-700/50 transition-colors cursor-pointer" data-order-id="${o.id}">
                  <td class="py-3.5 px-5">
                    <span class="font-mono text-xs font-semibold text-red-500 bg-red-500/10 px-2.5 py-1 rounded-lg">#${o.id.slice(0, 8).toUpperCase()}</span>
                  </td>
                  <td class="py-3.5 px-4 font-semibold text-white">${getUserName(o.userUid)}</td>
                  <td class="py-3.5 px-4 text-gray-400 text-xs">${o.items.length} item${o.items.length !== 1 ? 's' : ''}</td>
                  <td class="py-3.5 px-4 font-bold text-white">$${o.totalAmount.toFixed(2)}</td>
                  <td class="py-3.5 px-4">${statusBadge(o.status)}</td>
                  <td class="py-3.5 px-4 text-gray-500 text-xs">${formatDate(o.createdAt)}</td>
                  <td class="py-3.5 px-4 text-right">
                    <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </td>
                </tr>`).join('')}
            </tbody>
          </table>
        </div>`;
    }

    tableEl.addEventListener('click', (e) => {
      const row = e.target.closest('[data-order-id]');
      if (row) navigate(`/orders/${row.dataset.orderId}`);
    });

    const paginationEl = document.getElementById('pagination');
    if (!paginationEl) return;
    if (totalPages <= 1 && filtered.length > 0) {
      paginationEl.innerHTML = `<span class="text-sm text-gray-400">${filtered.length} order${filtered.length !== 1 ? 's' : ''}</span>`;
    } else {
      paginationEl.innerHTML = `
        <span class="text-sm text-gray-400">
          ${filtered.length === 0 ? 0 : (currentPage - 1) * PAGE_SIZE + 1}–${Math.min(currentPage * PAGE_SIZE, filtered.length)} of ${filtered.length}
        </span>
        <div class="flex gap-2">
          <button id="prev-page" ${currentPage <= 1 ? 'disabled' : ''}
            class="px-4 py-2 border border-gray-600 rounded-xl text-sm font-medium bg-gray-800 text-gray-300 ${currentPage <= 1 ? 'opacity-40 cursor-not-allowed' : 'hover:bg-gray-700'} transition-colors">Prev</button>
          <span class="px-3 py-2 text-sm font-medium text-gray-400">${currentPage} / ${totalPages}</span>
          <button id="next-page" ${currentPage >= totalPages ? 'disabled' : ''}
            class="px-4 py-2 border border-gray-600 rounded-xl text-sm font-medium bg-gray-800 text-gray-300 ${currentPage >= totalPages ? 'opacity-40 cursor-not-allowed' : 'hover:bg-gray-700'} transition-colors">Next</button>
        </div>`;

      document.getElementById('prev-page')?.addEventListener('click', () => {
        if (currentPage > 1) { currentPage--; renderTable(); }
      });
      document.getElementById('next-page')?.addEventListener('click', () => {
        if (currentPage < totalPages) { currentPage++; renderTable(); }
      });
    }
  }

  document.getElementById('status-filter').addEventListener('change', (e) => {
    statusFilter = e.target.value;
    currentPage = 1;
    renderStatusSummary();
    renderTable();
  });

  document.getElementById('search-input').addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    currentPage = 1;
    renderTable();
  });

  renderStatusSummary();
  renderTable();
}
