# Banking REST API — Full Stack Application

A full stack banking platform built with **FastAPI** (backend) and **React** (frontend), using **MySQL** as the database.

---

## Project Structure

```
banking-app/
├── banking-api/          ← FastAPI backend
│   ├── controllers/
│   │   ├── accounts.py
│   │   └── customers.py
│   ├── models/
│   │   └── models.py
│   ├── repository/
│   │   └── db_models.py
│   ├── services/
│   │   ├── account_service.py
│   │   └── customer_service.py
│   ├── database.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── banking-frontend/     ← React frontend
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── api/
    │   │   └── index.js
    │   ├── components/
    │   │   └── ConfirmDialog.js
    │   ├── pages/
    │   │   ├── Dashboard.js
    │   │   ├── Customers.js
    │   │   └── Accounts.js
    │   ├── App.js
    │   ├── index.js
    │   └── index.css
    └── package.json
```

---

## Prerequisites

Make sure you have the following installed before running the app:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | https://python.org |
| Node.js | 18+ (LTS) | https://nodejs.org |
| MySQL | 8.0+ | https://dev.mysql.com |

---

## Backend Setup

### 1. Create the MySQL database and user

Log into MySQL and run:

```sql
CREATE DATABASE bankdb;
CREATE USER 'bank_user'@'localhost' IDENTIFIED BY 'bank_pass123';
GRANT ALL PRIVILEGES ON bankdb.* TO 'bank_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configure environment variables

Create a `.env` file in the `banking-api/` folder:

```
DB_USER=bank_user
DB_PASSWORD=bank_pass123
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bankdb
```

### 3. Install Python dependencies

```bash
cd banking-api
pip install -r requirements.txt
```

### 4. Start the backend server

```bash
uvicorn main:app --reload --port 8000
```

The API will be running at http://localhost:8000

Interactive API docs (Swagger UI) are available at http://localhost:8000/docs

---

## Frontend Setup

### 1. Install Node dependencies

```bash
cd banking-frontend
npm install
```

### 2. Start the frontend

```bash
npm start
```

The app will open automatically at http://localhost:3000

---

## Running the Full Stack App

You need **two terminals open at the same time** — one for each server.

**Terminal 1 — Backend:**
```bash
cd banking-api
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd banking-frontend
npm start
```

Then open http://localhost:3000 in your browser.

> The frontend is configured to automatically proxy all `/api/` requests to the backend on port 8000, so no additional configuration is needed.

---

## Features

### Dashboard
- Total customer and account counts
- Total assets under management (AUM)
- Savings vs checking balance breakdown
- Top customers by balance
- Most recently opened accounts

### Customers
- View all customers in a sortable table
- Search by name or email
- Create new customers
- Edit existing customer name and email
- Delete customers (cascades to their accounts)
- Expand a customer row to view their linked accounts

### Accounts
- View all accounts across all customers
- Filter by account type (Savings / Checking)
- Search by account number or customer name
- Open new accounts and link them to a customer
- Edit account number, type, and balance
- Close (delete) accounts
- Running total of filtered balances shown in the table footer

---

## API Endpoints

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | Get all customers |
| GET | `/api/customers/{id}` | Get customer by ID |
| GET | `/api/customers/search?name=` | Search customers by name |
| POST | `/api/customers` | Create a new customer |
| PUT | `/api/customers/{id}` | Update a customer |
| DELETE | `/api/customers/{id}` | Delete a customer |

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts` | Get all accounts |
| GET | `/api/accounts/{id}` | Get account by ID |
| GET | `/api/accounts/search?name=` | Search accounts by customer name |
| POST | `/api/accounts` | Open a new account |
| PUT | `/api/accounts/{id}` | Update an account |
| DELETE | `/api/accounts/{id}` | Close an account |

---

## Troubleshooting

**Backend won't start — database connection error**
- Confirm MySQL is running
- Double-check your `.env` credentials
- Test the connection manually: `mysql -u bank_user -p bankdb`

**Frontend shows blank page or API errors**
- Make sure the backend is running on port 8000
- Check the browser console (F12) for error messages
- Confirm the `"proxy": "http://localhost:8000"` line is in `package.json`

**`npm install` fails**
- Make sure Node.js 18+ is installed: `node --version`
- Try deleting `node_modules/` and `package-lock.json`, then run `npm install` again

**Vulnerabilities warning after `npm install`**
- This is normal for React projects — the warnings relate to build tooling, not your running app
- Run `npm audit fix` to resolve most of them safely
- Do **not** run `npm audit fix --force`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, React Router, Axios |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | MySQL 8, PyMySQL |
| Styling | Custom CSS (no component library) |
