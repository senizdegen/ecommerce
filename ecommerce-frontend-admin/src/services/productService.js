import { apiGet, apiPostForm, apiPatchForm, apiDelete } from './api.js';
import { config } from '../config/config.js';
import { mockProducts } from '../storage/mockData.js';

function normalize(p) {
  return {
    id: p.uid || p.id,
    name: p.name,
    description: p.description,
    price: typeof p.price === 'string' ? parseFloat(p.price) : p.price,
    stock: p.available_quantity ?? p.availableQuantity ?? null,
    availableQuantity: p.available_quantity ?? p.availableQuantity ?? null,
    categoryName: p.category_name ?? p.category?.name ?? p.categoryName ?? null,
    categoryUid: p.category_uid ?? p.category?.uid ?? p.categoryUid ?? null,
    image: p.image_url ?? p.image ?? null,
    rating: p.rating ?? 0,
  };
}

let mockStore = [...mockProducts];

export async function getAll() {
  if (config.MOCK.products) return [...mockStore];
  const data = await apiGet(config.API.feed, '/products/');
  return data.map(normalize);
}

export async function getById(id) {
  if (config.MOCK.products) return mockStore.find((p) => p.id === id) || null;
  try {
    const data = await apiGet(config.API.feed, `/products/${id}`);
    return normalize(data);
  } catch {
    return null;
  }
}

export async function getCategories() {
  if (config.MOCK.products) {
    const seen = new Set();
    return mockStore
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

export async function createProduct(data) {
  if (config.MOCK.products) {
    const newProduct = {
      id: String(Date.now()),
      name: data.name,
      description: data.description,
      price: parseFloat(data.price),
      stock: parseInt(data.available_quantity, 10),
      availableQuantity: parseInt(data.available_quantity, 10),
      categoryName: null,
      categoryUid: null,
      image: null,
      rating: 0,
    };
    mockStore.push(newProduct);
    return newProduct;
  }

  const formData = new FormData();
  formData.append('name', data.name);
  formData.append('description', data.description);
  formData.append('price', String(parseFloat(data.price)));
  formData.append('available_quantity', String(parseInt(data.available_quantity, 10)));
  if (data.category_uid) formData.append('category_uid', data.category_uid);
  if (data.image) formData.append('image', data.image);

  return apiPostForm(config.API.product, '/products/', formData);
}

export async function updateProduct(id, data) {
  if (config.MOCK.products) {
    const idx = mockStore.findIndex((p) => p.id === id);
    if (idx === -1) throw new Error('Product not found');
    mockStore[idx] = {
      ...mockStore[idx],
      name: data.name,
      description: data.description,
      price: parseFloat(data.price),
    };
    return mockStore[idx];
  }

  const formData = new FormData();
  formData.append('name', data.name);
  formData.append('description', data.description);
  formData.append('price', String(parseFloat(data.price)));
  if (data.category_uid) formData.append('category_uid', data.category_uid);
  if (data.image) formData.append('image', data.image);

  const updated = await apiPatchForm(config.API.product, `/products/${id}`, formData);
  return normalize(updated);
}

export async function deleteProduct(id) {
  if (config.MOCK.products) {
    mockStore = mockStore.filter((p) => p.id !== id);
    return null;
  }
  return apiDelete(config.API.product, `/products/${id}`);
}