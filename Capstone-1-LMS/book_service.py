from datetime import datetime, timedelta

books = [
    {"id": 1, "title": "Harry Potter", "category": "Fiction"},
    {"id": 2, "title": "To Kill a Mockingbird", "category": "Fiction"},
    {"id": 3, "title": "Pride and Prejudice", "category": "Fiction"},
    {"id": 4, "title": "A Game Of Thrones", "category": "Fantasy"},
    {"id": 5, "title": "The Hobbit", "category": "Fantasy"},
    {"id": 6, "title": "The Name of the Wind", "category": "Fantasy"},
    {"id": 7, "title": "Ghosts of the Silent Hills", "category": "Horror"},
    {"id": 8, "title": "Dracula", "category": "Horror"},
    {"id": 9, "title": "The Haunting of Hill House", "category": "Horror"},
    {"id": 10, "title": "The Book Thief", "category": "Historical-Fiction"},
    {"id": 11, "title": "All the Light We Cannot See", "category": "Historical-Fiction"},
    {"id": 12, "title": "The Nightingale", "category": "Historical-Fiction"}
]

cart = []

def get_books():
    return books

def add_to_cart(selected_book_ids):
    global cart
    for book_id in selected_book_ids:
        book = next((book for book in books if str(book['id']) == book_id), None)
        if book and book not in cart:
            cart.append(book)

def get_cart():
    return cart

def calculate_due_date(start_date, days=30):
    current_date = start_date
    added_days = 0
    while added_days < days:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday are 0 to 4
            added_days += 1
    return current_date

def get_books_by_ids(book_ids):
    return [book for book in books if str(book['id']) in book_ids]
