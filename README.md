# POS Lite - Point of Sale & Inventory Management System

Aplikasi kasir dan manajemen stok sederhana dengan fitur transaksi, pelacakan inventory, dan dashboard reporting.

## Tech Stack

- **Frontend:** Vue 3.5 + Vite + Pinia + Vue Router + Chart.js + Axios
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL + JWT Auth
- **Database:** PostgreSQL 17

## Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 17 (opsional, project pake instance sendiri)

## Setup & Run

### 1. Start Database

Project ini pake PostgreSQL instance sendiri di port `5433` biar gak bentrok sama system PostgreSQL.

```bash
cd backend
/usr/lib/postgresql/17/bin/pg_ctl -D pgdata -l pgdata/logfile start
```

### 2. Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend akan jalan di `http://localhost:8000`  
Dokumentasi API (Swagger): `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
npm run dev
```

Frontend akan jalan di `http://localhost:5173`

### 4. Login

Register dulu, terus login pake akun yang udah dibuat.

## Default Flow

1. Buka `http://localhost:5173/register` → buat akun baru
2. `http://localhost:5173/login` → masuk pake akun
3. Dashboard → liat ringkasan penjualan
4. POS → pilih produk, masukin ke keranjang, checkout
5. Products → manage produk (admin only)
6. Categories → manage kategori (admin only)
7. Transactions → liat riwayat transaksi

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Current user |
| GET/POST | `/api/categories` | List / Create categories |
| GET/PUT/DELETE | `/api/categories/{id}` | Get / Update / Delete category |
| GET/POST | `/api/products` | List / Create products |
| GET/PUT/DELETE | `/api/products/{id}` | Get / Update / Delete product |
| PATCH | `/api/products/{id}/stock` | Update stock |
| GET/POST | `/api/transactions` | List / Create transactions |
| GET | `/api/transactions/{id}` | Transaction detail |
| GET | `/api/reports/summary` | Sales summary |
| GET | `/api/reports/sales-chart` | Sales chart data |
| GET | `/api/reports/top-products` | Top products |
| GET | `/api/reports/category-breakdown` | Sales by category |

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings (env)
│   ├── core/                # Database, security, dependencies
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── crud/                # Database operations
│   ├── api/v1/              # API routes
│   └── utils/               # Helpers
├── pgdata/                  # PostgreSQL data (local instance)
├── alembic/                 # Migrations
└── requirements.txt

frontend/
├── src/
│   ├── api/                 # Axios + API modules
│   ├── stores/              # Pinia (auth, cart)
│   ├── router/              # Vue Router
│   ├── layouts/             # AuthLayout, DashboardLayout
│   ├── views/               # Login, Register, Dashboard, POS, etc
│   ├── components/          # UI, layout, POS, dashboard components
│   └── utils/               # Formatters, validators
├── index.html
├── vite.config.js
└── package.json
```

## Role Access

- **Admin**: Full access (manage products, categories, view reports)
- **Cashier**: POS, transactions, view products & stock
