# API Documentation

![Flask](https://img.shields.io/badge/Flask-3.1.1-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-red)
![JWT](https://img.shields.io/badge/JWT_Extended-4.7.1-orange)

## Project Structure

```bash
backend/
├── app/
│ ├── routes/ 		# API endpoint definitions
│ ├──  init .py 	# Flask application factory
│ ├── config.py 	# Configuration settings
│ ├── models.py 	# Database models
│ └── schemas.py 	# Marshmallow schemas
├── migrations/ 	# Database migration scripts
├── test/ 		# Unit tests
├── requirements.txt 	# Python dependencies
└── run.py 		# Application entry point
```

## ✨Key Features

### 🔐Authentication

- JWT-based authentication
- User registration and login endpoints
- Password hashing
- Role-based access control

## 🚀API Endpoints

### 👥Users

| Endpoint                | Method | Description             |
| ----------------------- | ------ | ----------------------- |
| `/api/users/register` | POST   | Register new user       |
| `/api/users/login`    | POST   | Login and get JWT token |
| `/api/users/get`      | GET    | List all users          |

## 🛠️Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Python3-venv

### Installation

To install the project locally, simply run the `setup.sh` script.

### Dependencies

Full list in `requirementes.txt`

### Running the Application

```
flask run
```

### Testing

```
python -m pytest test/
```

## 🔒Security Features

* JWT authentication
* Password hashing
* Role-based access control
* Secure database configuration
* Environment variable protection
