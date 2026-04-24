import { apiGet, apiPatch, apiDelete } from './api.js';
import { config } from '../config/config.js';
import { mockUsers } from '../storage/mockData.js';

function normalize(c) {
  return {
    id: c.uid ?? c.id,
    firstName: c.first_name ?? c.firstName,
    lastName: c.last_name ?? c.lastName,
    email: c.email,
    isAdmin: c.is_admin ?? false,
    isVerified: c.is_verified ?? false,
    registeredDate: c.created_at
      ? new Date(c.created_at).toLocaleDateString()
      : (c.registeredDate ?? null),
  };
}

export async function findAllCustomers() {
  if (config.MOCK.customers) return mockUsers.map(normalize);
  const data = await apiGet(config.API.user, '/users/');
  return data.map(normalize);
}

export async function findCustomerById(id) {
  if (config.MOCK.customers) {
    return mockUsers.map(normalize).find(c => c.id === id) || null;
  }
  try {
    const data = await apiGet(config.API.user, `/users/${id}`);
    return normalize(data);
  } catch {
    return null;
  }
}

export async function updateCustomer(id, updateData) {
  if (config.MOCK.customers) {
    const customer = mockUsers.find(c => c.id === id);
    if (!customer) throw new Error('Customer not found');
    Object.assign(customer, updateData);
    return normalize(customer);
  }

  // updateData может содержать { first_name, last_name, email, is_admin }
  const data = await apiPatch(config.API.user, `/users/${id}`, updateData);
  return normalize(data);
}

export async function deleteCustomer(id) {
  if (config.MOCK.customers) {
    const idx = mockUsers.findIndex(c => c.id === id);
    if (idx === -1) throw new Error('Customer not found');
    mockUsers.splice(idx, 1);
    return null;
  }

  // DELETE на auth сервис — удаляет аккаунт
  await apiDelete(config.API.auth, `/auth/${id}`);
}