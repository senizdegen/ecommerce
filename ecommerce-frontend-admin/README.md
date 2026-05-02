# E-Commerce Admin Panel

Admin dashboard for managing products, orders, and customers.

Built with **Vite** + **Vanilla JS** + **Tailwind CSS**.

## Prerequisites

- Node.js 18+
- All backend microservices running:

| Service   | URL                          |
|----------|------------------------------|
| Auth     | http://localhost:8001        |
| User     | http://localhost:8002        |
| Product  | http://localhost:8003        |
| Cart     | http://localhost:8004        |
| Order    | http://localhost:8005        |
| Feed     | http://localhost:8007        |

---

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Start dev server
npm run dev
```

Open http://localhost:3001 in your browser.

---

## Configuration

Edit `src/config/config.js`:

```js
export const config = {
  API: {
    auth: 'http://localhost:8001/api/v1',
    user: 'http://localhost:8002/api/v1',
    product: 'http://localhost:8003/api/v1',
    feed: 'http://localhost:8007/api/v1/feed',
    cart: 'http://localhost:8004/api/v1',
    order: 'http://localhost:8005/api/v1',
  },

  MOCK: {
    auth: false,
    products: false,
    customers: false,
    orders: true,
  },

  APP_NAME: 'AdminPanel',
};
```

### Mock System

- true → uses localStorage / mock data  
- false → uses real backend API  

---

## Features

- Admin authentication
- Product management (CRUD)
- Customer management
- Order management (partial / mock support)
- Microservice-based API integration
- Mock + real API switching
- Dashboard UI

---

## Project Structure

```
src/
├── config/        # API + mock configuration
├── core/          # Auth, router, event bus
├── services/      # API calls (auth, products, orders, users)
├── pages/         # Admin pages
├── components/    # UI components (sidebar, modal, toast)
├── storage/       # Mock + localStorage
├── main.js        # Entry point
└── style.css      # Tailwind styles
```

---

## API Architecture

This admin panel communicates with multiple microservices:

- Auth Service
- User Service (customers)
- Product Service
- Cart Service
- Order Service
- Feed Service

---

## Build

```bash
npm run build
npm run preview
```

---

## Notes

This project is part of a full-stack ecommerce system:

- customer frontend
- admin panel (this repo)
- backend microservices


