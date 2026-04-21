import { apiGet, apiPost } from './api.js';
import { config } from '../config/config.js';
import { mockOrders } from '../storage/mockData.js';

let mockStore = mockOrders.map(o => ({ ...o, items: o.items.map(i => ({ ...i })) }));

function normalizeItem(item) {
  return {
    uid: String(item.uid),
    productUid: String(item.product_uid),
    quantity: item.quantity,
    priceSnapshot: parseFloat(item.price_snapshot),
  };
}

function normalizeOrder(entry) {
  const order = entry.order ?? entry;
  const items = entry.items ?? [];
  return {
    id: String(order.uid),
    userUid: String(order.user_uid),
    status: order.status,
    totalAmount: parseFloat(order.total_amount),
    createdAt: order.created_at,
    items: items.map(normalizeItem),
  };
}

export async function getAllOrders() {
  if (config.MOCK.orders) {
    return [...mockStore].sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  }
  const data = await apiGet(config.API.order, '/orders/admin/all');
  return data.map(normalizeOrder);
}

export async function cancelOrder(id) {
  if (config.MOCK.orders) {
    const order = mockStore.find(o => o.id === id);
    if (!order) throw new Error('Order not found');
    order.status = 'CANCELLED';
    return { ...order };
  }
  const data = await apiPost(config.API.order, `/orders/${id}/cancel`, null);
  return normalizeOrder(data);
}
