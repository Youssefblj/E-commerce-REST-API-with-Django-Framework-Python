# E-commerce REST API with Django

A powerful and scalable **E-commerce REST API** built using **Django** and **Django REST Framework**.
This project provides authentication, product management, orders system, reviews, and password reset via email.

---

# Features

## Authentication

* User Registration
* User Login
* JWT Authentication
* Update User Profile
* Password Reset via Email

## Products

* Create Product
* Update Product
* Delete Product
* Product List
* Product Details
* Search Products
* Filter Products
* Product Reviews & Ratings

## Orders

* Create New Order
* Get User Orders
* Get Order Details
* Delete Order

---

# Technologies Used

* Python
* Django
* Django REST Framework
* SQLite
* JWT Authentication
* Django Filter

---

# Project Structure

```bash
emarket/
│── account/
│── product/
│── order/
│── emarket/
│── manage.py
│── requirements.txt
│── README.md
```

---

# Installation

## 1 Clone Repository

```bash
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
```

## 2 Create Virtual Environment

```bash
python -m venv env
```

## 3 Activate Environment

### Windows

```bash
env\Scripts\activate
```

### Linux / Mac

```bash
source env/bin/activate
```

## 4 Install Requirements

```bash
pip install -r requirements.txt
```

## 5 Run Migrations

```bash
python manage.py migrate
```

## 6 Start Server

```bash
python manage.py runserver
```

---

# API Endpoints

## Account

* `/api/register/`
* `/api/userinfo/`
* `/api/userinfo/update/`
* `/api/forgot-password/`
* `/api/reset-password/<token>/`

## Products

* `/api/products/`
* `/api/products/<id>/`
* `/api/product/new/`
* `/api/product/update/<id>/`
* `/api/product/delete/<id>/`
* `/api/product/review/<id>/`

## Orders

* `/api/orders/`
* `/api/order/<id>/`
* `/api/order/new/`
* `/api/order/delete/<id>/`

---

# Authentication

Use JWT Token in headers:

```bash
Authorization: Bearer your_token_here
```

---

# Example Response

```json
{
  "id": 1,
  "name": "Laptop",
  "price": 1200,
  "stock": 5
}
```

---

# Future Improvements

* Payment Gateway Integration
* Cart System
* Wishlist
* Admin Dashboard
* Deployment

---

# Author

Developed by Youssef Blj

---

# License

This project is open-source and available under the MIT License.
