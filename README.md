# 🛒 Django Single Vendor E-Commerce Application

A full-featured **Single Vendor E-Commerce web application** built with **Django, MySQL, and Bootstrap**.  
This project includes product browsing, user authentication, cart management, order placement, and payment integration with **SSLCommerz**.

It is designed to be portfolio-ready and demonstrates a complete end-to-end Django application.

---

## 🚀 Features

### Home Page
- Fully functional navbar (Home, Cart, Login/Register)
- Product listing with:
  - Product name & description
  - Old price / New price
  - New Arrival badge
- Product detail page with image, price, and stock
- Footer with basic company information

### User Authentication
- Registration & Login with email & password
- Session-based authentication
- Login required for cart and order actions

### Product Management
- Add, edit, delete products (via Django admin)
- Upload product images
- Stock tracking and “Out of Stock” alerts
- New Arrival badge display

### Cart System
- Add products to cart
- Update quantity
- Remove items
- Cart total calculation
- Cart is linked to the logged-in user

### Order & Payment
- Place orders from cart
- Orders stored with associated OrderItems
- Cart cleared after order placement
- SSLCommerz payment integration (sandbox)
- Handles payment success, failure, and cancellation
- Order history with status tracking (Pending, Paid, Failed)

---

## 🧰 Tech Stack

- **Backend:** Django 5  
- **Frontend:** HTML, Bootstrap, Django Templates  
- **Database:** MySQL  
- **Authentication:** Django Auth  
- **Image Handling:** Pillow  
- **Payment Gateway:** SSLCommerz (Sandbox)  
- **Version Control:** Git & GitHub

---


## 🔐 Authentication

- Uses Django’s built-in `User` model
- Protected views use `@login_required`

