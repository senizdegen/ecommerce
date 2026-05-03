import { config } from '../config/config.js';
import { apiGet, apiPost } from './api.js';
import { lsGetAll, lsSet } from '../storage/localStorage.js';
import { clearCart } from './cartService.js';

const ORDERS_KEY = 'orders';

// ── Helpers ──────────────────────────────────────────────────────────────────

function normalizeApiOrder(order) {
  return {
    uid: String(order.uid),
    userUid: String(order.user_uid),
    status: order.status,
    totalAmount: parseFloat(order.total_amount),
    createdAt: order.created_at,
    updatedAt: order.updated_at,
  };
}

function normalizeApiItem(item) {
  return {
    uid: String(item.uid),
    orderUid: String(item.order_uid),
    productUid: String(item.product_uid),
    quantity: item.quantity,
    priceSnapshot: parseFloat(item.price_snapshot),
  };
}

// ── Mock implementations ─────────────────────────────────────────────────────

function mockCheckout(cartItems, total) {
  const orders = lsGetAll(ORDERS_KEY);
  const orderUid = 'o' + Date.now();

  const newOrder = {
    order: {
      uid: orderUid,
      status: 'PENDING',
      totalAmount: parseFloat(total.toFixed(2)),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    items: cartItems.map(item => ({
      uid: 'i' + Date.now() + Math.random(),
      orderUid,
      productUid: item.productId,
      name: item.name,
      image: item.image,
      quantity: item.qty,
      priceSnapshot: item.price,
    })),
  };

  orders.push(newOrder);
  lsSet(ORDERS_KEY, orders);
  clearCart();
  return newOrder;
}

function mockGetOrders() {
  return lsGetAll(ORDERS_KEY).map(entry => ({ ...entry.order, items: entry.items }));
}

function mockGetOrderByUid(uid) {
  const orders = lsGetAll(ORDERS_KEY);
  return orders.find(entry => entry.order.uid === String(uid)) || null;
}

function mockCancelOrder(uid) {
  const orders = lsGetAll(ORDERS_KEY);
  const entry = orders.find(e => e.order.uid === String(uid));

  if (!entry) return null;
  if (entry.order.status === 'CANCELLED') throw new Error('Order is already cancelled');
  if (entry.order.status === 'PAID') throw new Error('Paid order cannot be cancelled');

  entry.order.status = 'CANCELLED';
  entry.order.updatedAt = new Date().toISOString();
  lsSet(ORDERS_KEY, orders);
  return entry;
}

// ── Real API implementations ─────────────────────────────────────────────────

async function apiCheckout(cartItems, total) {
  const data = await apiPost(config.API.order, '/orders/checkout', {
    items: cartItems.map(item => ({
      product_uid: item.productId,
      quantity: item.qty,
      price_snapshot: item.price,
    })),
    total_amount: parseFloat(total.toFixed(2)),
  });

  return {
    order: normalizeApiOrder(data.order),
    items: data.items.map(normalizeApiItem),
  };
}

async function apiGetOrders() {
  const data = await apiGet(config.API.order, '/orders/');
  return data.map(normalizeApiOrder);
}

async function apiGetOrderByUid(uid) {
  const data = await apiGet(config.API.order, `/orders/${uid}`);
  return {
    order: normalizeApiOrder(data.order),
    items: data.items.map(normalizeApiItem),
  };
}

async function apiCancelOrder(uid) {
  const data = await apiPost(config.API.order, `/orders/${uid}/cancel`, null);
  return {
    order: normalizeApiOrder(data.order),
    items: data.items.map(normalizeApiItem),
  };
}

// ── Public API ────────────────────────────────────────────────────────────────
export async function checkout(cartItems, total) {
  if (config.MOCK.order) return mockCheckout(cartItems, total);
  const result = await apiCheckout(cartItems, total); // ← передать параметры
  clearCart();
  return result;
}

export async function getOrders() {
  return config.MOCK.order ? mockGetOrders() : apiGetOrders();
}

export async function getOrderByUid(uid) {
  return config.MOCK.order ? mockGetOrderByUid(uid) : apiGetOrderByUid(uid);
}

export async function cancelOrder(uid) {
  return config.MOCK.order ? mockCancelOrder(uid) : apiCancelOrder(uid);
}