# DSPL Asset Pulse - Backend API

## Architecture Overview

```

app/
├── init.py # Flask app factory
├── config/
│ └── init.py # Environment configs (dev, prod, test)
├── models/
│ ├── init.py # Model exports
│ ├── db.py # Database initialization
│ ├── user.py # User model with UserRole enum
│ ├── employee.py # Employee model with EmployeeStatus enum
│ ├── conference_room.py # ConferenceRoom model
│ └── booking.py # Booking model with BookingStatus enum
├── controllers/
│ ├── init.py # Controller exports
│ ├── auth_controller.py # Authentication request handlers
│ ├── user_controller.py # User management request handlers
│ ├── conference_room_controller.py # Conference room request handlers
│ └── booking_controller.py # Booking request handlers
├── services/
│ ├── init.py # Service exports
│ ├── auth_service.py # Authentication business logic
│ ├── user_service.py # User management business logic
│ ├── conference_room_service.py # Conference room business logic
│ └── booking_service.py # Booking business logic with conflict detection
├── routes/
│ ├── init.py # Blueprint registry
│ ├── auth.py # Auth endpoints
│ ├── sample.py # Sample protected endpoints
│ ├── user_routes.py # User management endpoints
│ ├── conference_room_routes.py # Conference room endpoints
│ └── booking_routes.py # Booking endpoints
└── utils/
├── jwt_utils.py # JWT token utilities & decorators
└── password_utils.py # Password verification
```

## Quick Start

### 1. Install Dependencies

Using uv:
```bash
uv sync
```


### 2. Run Development Server

```bash
python run.py
```
### 4. Seed Demo Users and Data
```bash
# Seed users only
python seed_db.py


```

#  API Endpoints

## Authentication

- **POST** `/api/v1/auth/register`  
  Register a new user

- **POST** `/api/v1/auth/login`  
  User login

- **POST** `/api/v1/auth/refresh`  
  Refresh access token


## Sample Protected Endpoints

- **GET** `/api/v1/sample/me`  
  Get current user

- **GET** `/api/v1/sample/employee-data`  
  Employee-only endpoint

- **GET** `/api/v1/sample/hr-data`  
  HR-only endpoint

- **GET** `/api/v1/sample/admin-data`  
  Admin-only endpoint


## User Management

- **POST** `/api/v1/users`  
  Create user (Admin/HR only)

- **GET** `/api/v1/users`  
  Get users with filters, pagination, and sorting (Admin/HR only)

- **GET** `/api/v1/users/<id>`  
  Get user by ID

- **PUT** `/api/v1/users/<id>`  
  Update user (Admin/HR only)

- **DELETE** `/api/v1/users/<id>`  
  Delete user (Admin only)


## Conference Room Management

- **POST** `/api/v1/conference-rooms`  
  Create conference room (Admin/HR only)

- **GET** `/api/v1/conference-rooms`  
  Get all conference rooms with pagination

- **GET** `/api/v1/conference-rooms/<id>`  
  Get conference room by ID

- **PUT** `/api/v1/conference-rooms/<id>`  
  Update conference room (Admin/HR only)

- **DELETE** `/api/v1/conference-rooms/<id>`  
  Delete conference room (Admin only)


## Booking Management

- **POST** `/api/v1/bookings`  
  Create a new booking (All authenticated users)

- **GET** `/api/v1/bookings/my-bookings`  
  Get current user's bookings

- **GET** `/api/v1/bookings/all`  
  Get all bookings (Admin/HR only)  
  Query params:
  - `upcoming_only=true` - Show only upcoming bookings
  - `upcoming_only=false` - Show all bookings (default)
  - `status=confirmed|complete|cancelled` - Filter by status

- **PUT** `/api/v1/bookings/<id>/cancel`  
  Cancel a booking

- **GET** `/api/v1/bookings/availability`  
  Check room availability for a date range


## Asset Management (FR-3)

- **POST** `/api/v1/assets`  
  Create asset (Admin/HR only)

- **GET** `/api/v1/assets`  
  Get all assets (Admin/HR only)

- **POST** `/api/v1/assets/<id>/assign`  
  Assign asset to employee (Admin/HR only)

- **POST** `/api/v1/assets/<id>/unassign`  
  Unassign (return) asset (Admin/HR only)

- **GET** `/api/v1/assets/employees/<id>/assets`  
  Get employee's assigned assets


---

#  Database Models

## User Model

| Field        | Type / Description |
|-------------|--------------------|
| `id`        | Primary Key |
| `email`     | Unique, Required, Indexed |
| `password`  | Required |
| `name`      | Optional |
| `role`      | Enum: `Employee`, `HR`, `Admin` |
| `created_at` | Timestamp |
| `updated_at` | Timestamp |
| `employee`  | One-to-one relationship with `Employee` |


## Employee Model

| Field              | Type / Description |
|-------------------|--------------------|
| `id`              | Primary Key |
| `user_id`         | Foreign Key to `User` (one-to-one) |
| `join_date`       | Date, Required |
| `separation_date` | Date, Optional |
| `status`          | Enum: `active`, `separated` |
| `created_at`      | Timestamp |
| `updated_at`      | Timestamp |
| `assignments`     | Relationship to `AssetAssignment` |


## ConferenceRoom Model

| Field        | Type / Description |
|-------------|--------------------|
| `id`        | Primary Key |
| `name`      | Unique, Required |
| `capacity`  | Integer, Required |
| `location`  | String, Optional |
| `is_active` | Boolean, Default: True |
| `created_at` | Timestamp |
| `bookings`  | Relationship to `Booking` |


## Booking Model

| Field        | Type / Description |
|-------------|--------------------|
| `id`        | Primary Key |
| `room_id`   | Foreign Key to `ConferenceRoom` |
| `user_id`   | Foreign Key to `User` |
| `start_time` | DateTime, Required |
| `end_time`  | DateTime, Required |
| `purpose`   | String(500), Required |
| `status`    | Enum: `confirmed`, `cancelled`, `complete` |
| `created_at` | Timestamp |
| `room`      | Relationship to `ConferenceRoom` |
| `user`      | Relationship to `User` |


## Asset Model (FR-3)

| Field        | Type / Description |
|-------------|--------------------|
| `id`        | Primary Key |
| `asset_code` | Unique, Required, Indexed |
| `asset_name` | Required |
| `asset_type` | Optional |
| `status`    | Enum: `available`, `assigned`, `maintenance` |
| `created_by` | Foreign Key to `User` |
| `created_at` | Timestamp |
| `updated_at` | Timestamp |
| `assignments` | Relationship to `AssetAssignment` |


## AssetAssignment Model (FR-3)

| Field         | Type / Description |
|--------------|--------------------|
| `id`         | Primary Key |
| `asset_id`   | Foreign Key to `Asset` |
| `employee_id` | Foreign Key to `Employee` |
| `assigned_by` | Foreign Key to `User` |
| `assigned_at` | Timestamp, Required |
| `returned_by` | Foreign Key to `User`, Optional |
| `returned_at` | Timestamp, Optional |
| `status`     | Enum: `assigned`, `returned` |
| `created_at` | Timestamp |
| `updated_at` | Timestamp |


##  Dependencies

Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS, Flask-JWT-Extended, Flasgger (Swagger UI), Werkzeug, python-dotenv, psycopg2-binary, cryptography, gunicorn


##  Demo Credentials

| Role     | Email                | Password    |
|----------|----------------------|-------------|
| Admin    | admin@company.com    | password123 |
| HR       | hr@company.com       | password123 |
| Employee | employee@company.com | password123 |


##  Swagger Documentation

Access interactive API documentation at: `http://localhost:5000/apidocs`
