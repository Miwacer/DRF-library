
# 📚 DRF Library API

A Django REST Framework-based backend for managing a library system.  
Includes user authentication, book catalog management, and borrowing operations.

---

## ⚙️ Features

- User registration & authentication
- Admin-only book creation/editing
- Book cover type (`HARD` / `SOFT`)
- Real-time inventory tracking
- Borrowing logic:
  - Borrow/Return
  - Inventory auto-decrement/increment
  - Telegram notification on borrow
- Admin can filter borrowings by `user_id` and `is_active`


---

## 🛠️ Setup Instructions

```bash
# Clone repo
git clone https://github.com/Miwacer/DRF-library.git
cd drf-library

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy sample env
cp .env.sample .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 🐳 Docker

```bash
# Build & run with docker-compose
docker-compose up --build
```

---

## 📦 Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- SQLite (local)
- Docker & Docker Compose
- Telegram Bot API (for notifications)

---

## 📬 Telegram Notification

When a user borrows a book, a message like this is sent to Telegram:

```
📚 New borrowing!

Book: The Alchemist

Expected return date: 2025-08-10
```

> Configure the bot token and chat ID in your `.env` file.

---

## ✅ To Do

- Filtering/sorting/searching for books
- Overdue return logic
- Email notifications
- API docs (Swagger / Redoc)

---

## 🧑‍💻 Author

Mykhailo Ostapenko  
GitHub: Miwacer

---

## 📜 License

MIT License – feel free to use and modify.
