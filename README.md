# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask, SQLAlchemy, and Marshmallow using the Application Factory Pattern.

## Tech Stack

- **Flask** – Web framework
- **Flask-SQLAlchemy** – ORM for MySQL database
- **Flask-Marshmallow / marshmallow-sqlalchemy** – Serialization & validation
- **Flask-Limiter** – Rate limiting
- **Flask-Caching** – Response caching
- **PyJWT** – JWT token authentication
- **MySQL** – Database
- **python-dotenv** – Environment variable management

## Project Structure

```
mechanic-shop-api/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── extensions.py        # Shared extension instances
│   ├── models.py            # SQLAlchemy models
│   ├── utils/
│   │   └── util.py          # JWT encode/decode & token_required decorator
│   └── blueprints/
│       ├── customers/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── mechanics/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── service_tickets/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       └── inventory/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
├── app.py                   # Entry point
├── config.py                # Configuration classes
├── requirements.txt
└── .env                     # Local credentials (not committed)
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/max-zaki/mechanic-shop-api.git
cd mechanic-shop-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (this file is git-ignored):

```
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=mechanics_db
```

### 5. Create the MySQL database

```sql
CREATE DATABASE mechanics_db;
```

### 6. Run the application

```bash
python app.py
```

The API will start at `http://127.0.0.1:5000`. Database tables are created automatically on first run.

---

## Authentication

Protected routes require a JWT Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Obtain a token by logging in via `POST /customers/login`.

---

## API Endpoints

### Customers — `/customers`

| Method | Endpoint                  | Auth Required | Description                              |
|--------|---------------------------|:-------------:|------------------------------------------|
| POST   | `/customers/login`        |               | Login and receive a JWT token            |
| POST   | `/customers/`             |               | Create a new customer *(5/day limit)*    |
| GET    | `/customers/`             |               | Get all customers *(paginated, cached)*  |
| GET    | `/customers/<id>`         |               | Get a specific customer                  |
| GET    | `/customers/my-tickets`   | ✓             | Get the logged-in customer's tickets     |
| PUT    | `/customers/`             | ✓             | Update the logged-in customer's account  |
| DELETE | `/customers/`             | ✓             | Delete the logged-in customer's account  |

Pagination query params for `GET /customers/`: `?page=1&per_page=10`

### Mechanics — `/mechanics`

| Method | Endpoint                  | Description                                    |
|--------|---------------------------|------------------------------------------------|
| POST   | `/mechanics/`             | Create a new mechanic                          |
| GET    | `/mechanics/`             | Get all mechanics                              |
| GET    | `/mechanics/most-worked`  | Get mechanics ranked by number of tickets      |
| PUT    | `/mechanics/<id>`         | Update a mechanic                              |
| DELETE | `/mechanics/<id>`         | Delete a mechanic                              |

### Service Tickets — `/service-tickets`

| Method | Endpoint                                                     | Description                              |
|--------|--------------------------------------------------------------|------------------------------------------|
| POST   | `/service-tickets/`                                          | Create a new service ticket              |
| GET    | `/service-tickets/`                                          | Get all service tickets                  |
| PUT    | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket            |
| PUT    | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket          |
| PUT    | `/service-tickets/<ticket_id>/edit`                          | Bulk add/remove mechanics on a ticket    |
| PUT    | `/service-tickets/<ticket_id>/add-part/<part_id>`            | Add an inventory part to a ticket        |

### Inventory — `/inventory`

| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| POST   | `/inventory/`         | Add a new part           |
| GET    | `/inventory/`         | Get all parts            |
| GET    | `/inventory/<id>`     | Get a specific part      |
| PUT    | `/inventory/<id>`     | Update a part            |
| DELETE | `/inventory/<id>`     | Delete a part            |

---

## Sample Request Bodies

### Login
```json
{
  "email": "jane@example.com",
  "password": "secret123"
}
```

### Create Customer
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "555-1234",
  "password": "secret123"
}
```

### Create Mechanic
```json
{
  "name": "Bob Torres",
  "email": "bob@shop.com",
  "phone": "555-9876",
  "salary": 55000.00
}
```

### Create Service Ticket
```json
{
  "vin": "1HGBH41JXMN109186",
  "svc_date": "2025-06-01",
  "svc_desc": "Oil change and tire rotation",
  "customer_id": 1
}
```

### Bulk Edit Mechanics on a Ticket
```json
{
  "add_ids": [2, 3],
  "remove_ids": [1]
}
```

### Create Inventory Part
```json
{
  "name": "Oil Filter",
  "price": 12.99
}
```
