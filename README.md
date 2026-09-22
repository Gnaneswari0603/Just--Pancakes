# 🥞 Just Pancakes

A simple and responsive **online pancake ordering website** built with **Django**.
Users can browse pancakes, add items to a cart, place orders, and choose between Cash on Delivery or online payment using Razorpay.

## ✨ Features

* 🏠 Home page
* 🥞 Pancake menu
* 🛒 Shopping cart
* ➕ Increase/decrease cart quantity
* 💰 Automatic cart total calculation
* 📝 Checkout form
* 📦 Order and Order Item management
* 💵 Cash on Delivery
* 💳 Razorpay online payment
* 🔐 Server-side Razorpay payment verification
* 👨‍💼 Django Admin Panel
* 📋 View orders and order items from the admin panel
* 🔒 Environment variables for sensitive payment credentials

## 🛠️ Technologies Used

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite

### Payment Gateway

* Razorpay

### Development Tools

* Git
* GitHub
* VS Code

## 📁 Project Structure

```text
Just--Pancakes/
│
├── core/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── just_pancakes/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

> `.env`, `db.sqlite3`, and virtual-environment files are intentionally excluded from the repository.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Gnaneswari0603/Just--Pancakes.git
```

### 2. Open the project

```bash
cd Just--Pancakes
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create the environment file

Create a `.env` file in the same folder as `manage.py`:

```env
RAZORPAY_KEY_ID=your_razorpay_test_key
RAZORPAY_KEY_SECRET=your_razorpay_test_secret
```

For security, never commit the `.env` file to GitHub.

### 7. Apply migrations

```bash
python manage.py migrate
```

### 8. Create an admin user

```bash
python manage.py createsuperuser
```

Follow the prompts to create your Django admin account.

### 9. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 💳 Razorpay Test Mode

The project supports Razorpay online payments.

For local development, use **Razorpay Test Mode** credentials in `.env`.

Do not use real payment credentials in the source code or commit them to GitHub.

## 🗃️ Database Models

The project currently uses the following main models:

### Product

Stores pancake product information such as:

* Name
* Price
* Image

### CartItem

Stores:

* Product
* Quantity

### Order

Stores:

* Customer name
* Phone number
* Address
* Order total
* Payment status
* Razorpay order ID
* Razorpay payment ID
* Order creation date

### OrderItem

Stores the individual products and quantities belonging to an order.

## 🔐 Security

Sensitive files are excluded using `.gitignore`.

The following files/directories are not committed:

```text
.env
db.sqlite3
.venv/
__pycache__/
```

Payment credentials should always be stored using environment variables.

## 📸 Application Flow

```text
Home
  ↓
Menu
  ↓
Add Pancakes to Cart
  ↓
Cart
  ↓
Checkout
  ↓
Choose Payment Method
  ├── Cash on Delivery
  │      ↓
  │   Order Created
  │
  └── Razorpay
         ↓
      Payment
         ↓
   Server-side Verification
         ↓
      Order Created
```

## 🔮 Future Improvements

* User registration and login
* User order history
* Order tracking
* Product categories
* Product search and filtering
* Better mobile responsiveness
* Coupon and discount system
* Delivery status management
* Improved payment and order notifications
* Deployment to a production server

## 👩‍💻 Author

**Gnaneswari**

GitHub:
https://github.com/Gnaneswari0603

## 📄 License

This project is created for learning and portfolio purposes.
