# Mechanic Shop API

A RESTful API for managing a mechanic shop built with Flask, SQLAlchemy, and Marshmallow using the Application Factory Pattern.

## Tech Stack

- **Flask** – Web framework
- **Flask-SQLAlchemy** – ORM for MySQL database
- **Flask-Marshmallow / marshmallow-sqlalchemy** – Serialization & validation
- **MySQL** – Database
- **python-dotenv** – Environment variable management

## Project Structure

```
mechanic-shop-api/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── extensions.py        # Marshmallow instance
│   ├── models.py            # SQLAlchemy models
│   └── blueprints/
│       ├── customers/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── mechanics/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       └── service_tickets/
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

The API will start at `http://127.0.0.1:5000`. The database tables are created automatically on first run.

---

## API Endpoints

### Customers — `/customers`

| Method | Endpoint               | Description            |
|--------|------------------------|------------------------|
| POST   | `/customers/`          | Create a new customer  |
| GET    | `/customers/`          | Get all customers      |
| GET    | `/customers/<id>`      | Get a specific customer|
| PUT    | `/customers/<id>`      | Update a customer      |
| DELETE | `/customers/<id>`      | Delete a customer      |

### Mechanics — `/mechanics`

| Method | Endpoint               | Description            |
|--------|------------------------|------------------------|
| POST   | `/mechanics/`          | Create a new mechanic  |
| GET    | `/mechanics/`          | Get all mechanics      |
| PUT    | `/mechanics/<id>`      | Update a mechanic      |
| DELETE | `/mechanics/<id>`      | Delete a mechanic      |

### Service Tickets — `/service-tickets`

| Method | Endpoint                                              | Description                        |
|--------|-------------------------------------------------------|------------------------------------|
| POST   | `/service-tickets/`                                   | Create a new service ticket        |
| GET    | `/service-tickets/`                                   | Get all service tickets            |
| PUT    | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a ticket |
| PUT    | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a ticket |

---

## Sample Request Bodies

### Create Customer
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "555-1234"
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
