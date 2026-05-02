<h1 align="center">🛒 E-Commerce Microservices Platform</h1>

<p align="center">
  Scalable microservices-based e-commerce backend built with FastAPI, PostgreSQL, RabbitMQ, and async Python.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-Backend-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Async-green?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql" />
  <img src="https://img.shields.io/badge/RabbitMQ-Event--Driven-orange?style=for-the-badge&logo=rabbitmq" />
  <img src="https://img.shields.io/badge/Architecture-Microservices-black?style=for-the-badge" />
</p>

---

## 📌 About The Project

This project is a backend system for an e-commerce platform built with a **microservices architecture**.

Each business domain is separated into an independent service with its own responsibility, which makes the system more scalable, maintainable, and closer to real production design.

The project focuses on:
- service isolation
- asynchronous APIs
- event-driven communication
- stock reservation logic
- clean backend architecture

---

## 🧩 Services

The system consists of the following services:

- **Auth Service** — handles authentication and JWT
- **Users Service** — manages user profiles
- **Products Service** — manages products
- **Inventory Service** — tracks stock and reservations
- **Cart Service** — manages user carts
- **Orders Service** — creates and processes orders
- **Feed Service** — provides read-optimized product data for frontend usage

---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- SQLModel
- SQLAlchemy Async
- PostgreSQL
- RabbitMQ
- aio-pika
- Uvicorn
- Alembic

### Architecture & Concepts
- Microservices
- Event-Driven Architecture
- Publish/Subscribe messaging
- Separate database per service
- Read-optimized feed model
- Async communication
- Inventory reservation flow

---

## 🏗️ Architecture Idea

This project follows a **microservices-based design**, where each service is responsible only for its own domain.

For example:
- the **Products Service** creates a product
- then publishes an event
- the **Inventory Service** reacts to that event and creates stock data
- the **Feed Service** consumes product events and builds a read-friendly product view for frontend requests

This approach reduces coupling between services and improves scalability.

---

## 🔄 Event-Driven Flow

Example product creation flow:

1. A product is created in **Products Service**
2. The service publishes a `product.created` event via RabbitMQ
3. **Inventory Service** consumes the event and creates inventory for the product
4. **Feed Service** consumes the same event and updates its read model
5. Frontend reads product data from **Feed Service**

---

## 📦 Main Features

- JWT-based authentication
- User profile creation flow
- Product management
- Inventory management
- Stock reservation logic
- Cart operations
- Order creation
- Price snapshot support in orders
- Event-driven synchronization between services
- Read-optimized product feed for frontend integration

---

## 🧠 Design Highlights

- **Database per service** for better isolation
- **RabbitMQ messaging** for async communication
- **Reserved quantity logic** to prevent overselling
- **Feed Service** as a separate read model for product queries
- **Async FastAPI services** for better performance
- Clear separation between write services and read-focused service

---

## Team Members
- 230103192
- 230103291
- 230103102
- 230103290

---


