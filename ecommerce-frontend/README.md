# E-Commerce Frontend

Customer-facing frontend for browsing products, managing cart, and placing orders.

Built with **Vite** + **Vanilla JS** + **Tailwind CSS**.

## Prerequisites

- Node.js 18+
- All backend microservices running:

| Service   | URL                          |
|----------|------------------------------|
| Auth     | http://localhost:8001        |
| User     | http://localhost:8002        |
| Product  | http://localhost:8003        |
| Cart     | http://localhost:8005        |
| Order    | http://localhost:8006        |
| Feed     | http://localhost:8007        |

---

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Start dev server
npm run dev
```

Open http://localhost:3000 in your browser.

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
    cart: 'http://localhost:8005/api/v1',
    order: 'http://localhost:8006/api/v1',
  },

  APP_NAME: 'Shopify',

  MOCK: {
    auth: false,
    user: true,
    product: false,
    cart: false,
    order: true,
    customer: true,
  }
};
```

### Mock System

- true → uses localStorage / mock data  
- false → uses real backend API  

---

## Features

- Product listing
- Product details page
- Cart management
- Order creation (partially implemented)
- Microservice-based API integration
- Mock + real API switching
- Responsive UI (Tailwind CSS)

---

## Project Structure

```
src/
├── config/        # API + mock configuration
├── core/          # Router, event system
├── services/      # API calls (per microservice)
├── pages/         # UI pages
├── components/    # UI components (navbar, footer, etc.)
├── storage/       # Mock + localStorage
├── main.js        # Entry point
└── style.css      # Tailwind styles
```

---

## API Architecture

This frontend communicates with multiple microservices:

- Auth Service
- User Service
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

- customer frontend (this repo)
- admin panel
- backend microservices

Project is still in development.
