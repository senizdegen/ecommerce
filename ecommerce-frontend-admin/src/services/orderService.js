import { apiGet, apiPost } from './api.js';
import { config } from '../config/config.js';

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
  const data = await apiGet(config.API.order, '/orders/admin/all');
  return data.map(normalizeOrder);
}

export async function cancelOrder(id) {
  const data = await apiPost(config.API.order, `/orders/${id}/cancel`, null);
  return normalizeOrder(data);
}
