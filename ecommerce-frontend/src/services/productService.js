import { apiGet } from './api.js';
import { config } from '../config/config.js';
import { lsGetAll } from '../storage/localStorage.js';

function normalize(p) {
  const availableQuantity = p.available_quantity ?? p.availableQuantity ?? 0;

  return {
    id: p.uid ?? p.id,
    name: p.name,
    description: p.description,
    price: typeof p.price === 'string' ? parseFloat(p.price) : p.price,
    availableQuantity,
    stock: availableQuantity,
    inStock: availableQuantity > 0,
    categoryName: p.category_name ?? p.category?.name ?? p.categoryName ?? null,
    categoryUid: p.category_uid ?? p.category?.uid ?? p.categoryUid ?? null,
    image: p.image_url ?? p.image ?? null,
    createdAt: p.created_at ?? null,
    updatedAt: p.updated_at ?? null,
  };
}

export async function getAll() {
  if (config.MOCK.product) {
    return lsGetAll('products').map(normalize);
  }
  const raw = await apiGet(config.API.feed, '/products/');
  return raw.map(normalize);
}

export async function getById(id) {
  if (config.MOCK.product) {
    const products = lsGetAll('products');
    const found = products.find(p => String(p.id) === String(id));
    return found ? normalize(found) : null;
  }
  try {
    const raw = await apiGet(config.API.feed, `/products/${id}`);
    return normalize(raw);
  } catch {
    return null;
  }
}

export async function getCategories() {
  if (config.MOCK.product) {
    const products = lsGetAll('products');
    const seen = new Set();
    return products
      .filter(p => p.categoryName)
      .filter(p => {
        if (seen.has(p.categoryName)) return false;
        seen.add(p.categoryName);
        return true;
      })
      .map(p => ({ uid: p.categoryUid ?? null, name: p.categoryName }));
  }
  try {
    return await apiGet(config.API.product, '/products/categories');
  } catch {
    return [];
  }
}

export async function getFeatured() {
  return (await getAll()).slice(0, 4);
}