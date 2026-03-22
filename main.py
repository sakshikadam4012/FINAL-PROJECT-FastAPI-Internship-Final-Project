from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import Query

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basics", "author": "John Doe", "genre": "Tech", "is_available": True},
    {"id": 2, "title": "History of India", "author": "R Sharma", "genre": "History", "is_available": True},
    {"id": 3, "title": "AI Revolution", "author": "Elon Musk", "genre": "Tech", "is_available": True},
    {"id": 4, "title": "Science World", "author": "A Einstein", "genre": "Science", "is_available": True},
    {"id": 5, "title": "Fiction Story", "author": "JK Rowling", "genre": "Fiction", "is_available": True},
    {"id": 6, "title": "Data Science", "author": "Andrew Ng", "genre": "Tech", "is_available": True},
]
# Queue for waiting users
queue = []


# Model for borrowing a book
class BorrowRequest(BaseModel):

    # Name of member (minimum 2 characters)
    member_name: str = Field(..., min_length=2)

    # Book ID must be greater than 0
    book_id: int = Field(..., gt=0)

    # Borrow days (1 to 30)
    borrow_days: int = Field(..., gt=0, le=60)

    # Member ID (minimum 4 characters)
    member_id: str = Field(..., min_length=4)

    member_type: str = "regular"  # default value


# Model for adding a new book
class NewBook(BaseModel):

    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    is_available: bool = True  # default value


# Helper function to find a book by ID
def find_book(book_id):

    for book in books:
        if book["id"] == book_id:
            return book  # Return book if found

    return None  # If not found


# Helper function to calculate due date
def calculate_due_date(days, member_type):

    if member_type == "premium":
        return f"Return within {min(days, 60)} days"

    return f"Return within {min(days, 30)} days"


# Task 1
@app.get("/")
def home():
    return {"message": "Welcome to Library System"}


# Task 2 - Get all books in the library
@app.get("/books")
def get_books():

    # Count how many books are available
    available_count = 0
    for book in books:
        if book["is_available"]:
            available_count += 1

    # Return total books + available books + full list
    return {
        "total_books": len(books),
        "available_books": available_count,
        "books": books,
    }


# Summary of all books
@app.get("/books/summary")
def get_summary():

    total = len(books)
    available = 0

    # Count available books
    for book in books:
        if book["is_available"]:
            available += 1

    borrowed = total - available

    # Count books by genre
    genre_count = {}

    for book in books:
        genre = book["genre"]

        if genre in genre_count:
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1

    return {
        "total_books": total,
        "available_books": available,
        "borrowed_books": borrowed,
        "genre_breakdown": genre_count,
    }


# Filter books based on given conditions
@app.get("/books/filter")
def filter_books(
    genre: str = Query(None),
    author: str = Query(None),
    is_available: bool = Query(None),
):

    result = books

    # Filter by genre
    if genre is not None:
        result = [b for b in result if b["genre"] == genre]

    # Filter by author
    if author is not None:
        result = [b for b in result if b["author"] == author]

    # Filter by availability
    if is_available is not None:
        result = [b for b in result if b["is_available"] == is_available]

    return {"total": len(result), "books": result}


# Add a new book
@app.post("/books")
def add_book(data: NewBook):

    # Check for duplicate title (case-insensitive)
    for book in books:
        if book["title"].lower() == data.title.lower():
            return {"error": "Book with this title already exists"}

    # Generate new ID
    new_id = max([b["id"] for b in books]) + 1

    # Create new book
    new_book = {
        "id": new_id,
        "title": data.title,
        "author": data.author,
        "genre": data.genre,
        "is_available": data.is_available,
    }

    # Add to list
    books.append(new_book)

    return {"message": "Book added successfully", "book": new_book}


# Add user to queue
@app.post("/queue/add")
def add_to_queue(member_name: str, book_id: int):

    # Find book
    book = find_book(book_id)

    if not book:
        return {"error": "Book not found"}

    # Only allow if book is not available
    if book["is_available"]:
        return {"message": "Book is available, no need to join queue"}

    # Add to queue
    queue.append({"member_name": member_name, "book_id": book_id})

    return {"message": "Added to queue successfully", "queue": queue}


# Return a book
@app.post("/return/{book_id}")
def return_book(book_id: int):

    # Find book
    book = find_book(book_id)

    if not book:
        return {"error": "Book not found"}

    # Mark book as available
    book["is_available"] = True

    # Check queue for this book
    for person in queue:
        if person["book_id"] == book_id:

            # Assign book to first waiting user
            book["is_available"] = False

            # Remove from queue
            queue.remove(person)

            # Add to borrow records
            global record_counter

            record = {
                "record_id": record_counter,
                "member_name": person["member_name"],
                "book_title": book["title"],
                "borrow_days": 5,
                "due_date": calculate_due_date(5, "regular"),
            }

            borrow_records.append(record)
            record_counter += 1

            return {
                "message": "Book returned and assigned to next user",
                "assigned_to": person["member_name"],
            }

    # If no one in queue
    return {"message": "Book returned and is now available"}


# Get queue list
@app.get("/queue")
def get_queue():

    return {"total": len(queue), "queue": queue}


# Update a book
@app.put("/books/{book_id}")
def update_book(
    book_id: int, genre: str = Query(None), is_available: bool = Query(None)
):

    # Find the book
    book = find_book(book_id)

    # If not found
    if not book:
        return {"error": "Book not found"}

    # Update only if value is provided
    if genre is not None:
        book["genre"] = genre

    if is_available is not None:
        book["is_available"] = is_available

    return {"message": "Book updated successfully", "book": book}


# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    # Find the book
    book = find_book(book_id)

    # If not found
    if not book:
        return {"error": "Book not found"}

    # Remove from list
    books.remove(book)

    return {"message": f"Book '{book['title']}' deleted successfully"}


# Search books by keyword
@app.get("/books/search")
def search_books(keyword: str):

    result = []

    for book in books:
        # Case-insensitive search
        if (
            keyword.lower() in book["title"].lower()
            or keyword.lower() in book["author"].lower()
        ):
            result.append(book)

    # If no result
    if not result:
        return {"message": "No books found"}

    return {"total": len(result), "books": result}


# Sort books by title or author
@app.get("/books/sort")
def sort_books(
    sort_by: str = "title",  # default sort by title
    order: str = "asc",  # default ascending
):

    # Sort logic
    sorted_books = sorted(
        books, key=lambda b: b[sort_by].lower(), reverse=(order == "desc")
    )

    return {"sorted_by": sort_by, "order": order, "books": sorted_books}


# Pagination for books
@app.get("/books/page")
def get_books_page(page: int = 1, limit: int = 3):

    # Calculate starting index
    start = (page - 1) * limit

    # Slice books list
    paginated_books = books[start : start + limit]

    return {
        "page": page,
        "limit": limit,
        "total_books": len(books),
        "books": paginated_books,
    }


# Search borrow records by member name
@app.get("/borrow-records/search")
def search_borrow_records(member_name: str):

    result = []

    # Loop through borrow records
    for record in borrow_records:
        if member_name.lower() in record["member_name"].lower():
            result.append(record)

    # If no records found
    if not result:
        return {"message": "No records found"}

    return {"total": len(result), "records": result}


# Pagination for borrow records
@app.get("/borrow-records/page")
def get_borrow_records_page(page: int = 1, limit: int = 3):

    start = (page - 1) * limit

    paginated = borrow_records[start : start + limit]

    return {
        "page": page,
        "limit": limit,
        "total_records": len(borrow_records),
        "records": paginated,
    }


@app.get("/books/browse")
def browse_books(
    keyword: str = Query(None),
    sort_by: str = Query("title"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):

    result = books

    # STEP 1: SEARCH
    if keyword:
        result = [
            b
            for b in result
            if keyword.lower() in b["title"].lower()
            or keyword.lower() in b["author"].lower()
        ]

    # STEP 2: SORT
    if sort_by not in ["title", "author", "genre"]:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False

    result = sorted(result, key=lambda b: b[sort_by], reverse=reverse)

    # STEP 3: PAGINATION
    total = len(result)
    start = (page - 1) * limit
    paginated = result[start : start + limit]

    total_pages = (total + limit - 1) // limit

    # RESPONSE
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": total_pages,
        "books": paginated,
    }


# Get a single book using its ID
@app.get("/books/{book_id}")
def get_book(book_id: int):

    # Loop through books list
    for book in books:
        if book["id"] == book_id:
            return book  # Return book if found

    # If book not found
    return {"error": "Book not found"}


# List to store borrow records (initially empty)
borrow_records = []


# Get all borrow records
@app.get("/borrow-records")
def get_borrow_records():

    # Return total records and list
    return {"total_records": len(borrow_records), "records": borrow_records}


# Counter for borrow records
record_counter = 1


# Borrow a book
@app.post("/borrow")
def borrow_book(data: BorrowRequest):

    global record_counter

    # Find the book using helper function
    book = find_book(data.book_id)

    # Check if book exists
    if not book:
        return {"error": "Book not found"}

    # Check if book is available
    if not book["is_available"]:
        return {"error": "Book is already borrowed"}

    # Mark book as borrowed
    book["is_available"] = False

    # Create borrow record
    record = {
        "record_id": record_counter,
        "member_name": data.member_name,
        "member_id": data.member_id,
        "book_title": book["title"],
        "borrow_days": data.borrow_days,
        "due_date": calculate_due_date(data.borrow_days, data.member_type),
    }

    # Add record to list
    borrow_records.append(record)

    # Increase counter
    record_counter += 1

    return {"message": "Book borrowed successfully", "record": record}