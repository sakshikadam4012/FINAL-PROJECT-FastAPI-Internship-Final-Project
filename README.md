📚 City Public Library API (FastAPI Project)

🚀 Overview

This project is a Library Management System API built using FastAPI.
It allows users to manage books, borrow records, queues, and perform advanced operations like search, sorting, and pagination.

---

🛠️ Tech Stack

- Python 🐍
- FastAPI ⚡
- Pydantic 📦
---

📂 Project Structure

project/
│── main.py
│── README.md

---

▶️ How to Run the Project

1. Install dependencies

pip install fastapi uvicorn

2. Run the server

uvicorn main:app --reload

3. Open in browser

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

📌 Features

✅ Beginner (Day 1)

- GET "/" → Welcome message
- GET "/books" → List all books
- GET "/books/{book_id}" → Get book by ID
- GET "/borrow-records" → View borrow records
- GET "/books/summary" → Summary of books

---

✅ Easy (Day 2–3)

- Pydantic validation ("BorrowRequest")
- POST "/borrow" → Borrow a book
- Helper functions:
  - "find_book()"
  - "calculate_due_date()"
- GET "/books/filter" → Filter books

---

✅ Medium (Day 4–5)

- POST "/books" → Add new book
- PUT "/books/{book_id}" → Update book
- DELETE "/books/{book_id}" → Delete book
- Queue system:
  - POST "/queue/add"
  - GET "/queue"
- POST "/return/{book_id}" → Return & auto-assign

---

✅ Hard (Day 6)

- GET "/books/search" → Search books
- GET "/books/sort" → Sort books
- GET "/books/page" → Pagination
- GET "/borrow-records/search"
- GET "/borrow-records/page"
- GET "/books/browse" → Combined filter + sort + pagination

---

📊 Example Book Data

{
  "id": 1,
  "title": "Python Basics",
  "author": "John Doe",
  "genre": "Tech",
  "is_available": true
}

---

🔁 Borrow Workflow

1. User sends request to "/borrow"
2. Check:
   - Book exists
   - Book is available
3. Mark book unavailable
4. Generate due date
5. Store borrow record

---

⏳ Queue System

- If book is unavailable → user added to queue
- When returned:
  - Automatically assigned to next user

---

🔍 Advanced Features

- Case-insensitive search
- Sorting (title, author, genre)
- Pagination support
- Combined browsing endpoint

---

❗ Validation Rules

- "member_name" ≥ 2 characters
- "book_id" > 0
- "borrow_days":
  - Regular → max 30 days
  - Premium → max 60 days

---

🧪 Testing

Use:

- Swagger UI ("/docs")
- Postman
- Curl

---

🎯 Learning Outcomes

- FastAPI basics
- REST API design
- Data validation with Pydantic
- CRUD operations
- Real-world workflow handling
- API optimization (search, sort, pagination)

---

📌 Future Improvements

- Database integration (SQLite/PostgreSQL)
- Authentication (JWT)
- Admin dashboard
- Book categories management

---

👩‍💻 Author

Sakshi Kadam

