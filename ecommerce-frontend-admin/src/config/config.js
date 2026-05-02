export const config = {
  API: {
    auth: import.meta.env.VITE_API_AUTH,
    user: import.meta.env.VITE_API_USER,
    product: import.meta.env.VITE_API_PRODUCT,
    feed: import.meta.env.VITE_API_FEED,
    cart: import.meta.env.VITE_API_CART,
    order: import.meta.env.VITE_API_ORDER,
  },

  APP_NAME: 'Shopify Admin Panel',

  MOCK: {
    auth: false,
    products: false,
    customers: false,
    orders: false,
  }
};
