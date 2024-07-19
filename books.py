from fastapi import Body, FastAPI
import json
from typing import List, Dict, Any
import os

app = FastAPI()

FILE_PATH = 'books_data.json'

INITIAL_BOOKS = [
    {"title": "Title one", "author": "Author one", "category": "science"},
    {"title": "Title two", "author": "Author two", "category": "science"},
    {"title": "Title three", "author": "Author three", "category": "history"},
    {"title": "Title four", "author": "Author four", "category": "math"},
    {"title": "Title five", "author": "Author five", "category": "math"},
    {"title": "Title six", "author": "Author two", "category": "math"}
]

def load_books() -> List[Dict[str, Any]]:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        # Save initial books to the file if it does not exist
        save_books(INITIAL_BOOKS)
        return INITIAL_BOOKS

def save_books(books: List[Dict[str, Any]]):
    with open(FILE_PATH, 'w') as file:
        json.dump(books, file, indent=4)

# Initialize BOOKS with data from file or initial data
BOOKS = load_books()

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}

@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get('/books/{book_author}/category')
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post('/books/create_book')
async def create_book(new_book: Dict[str, Any] = Body()):
    BOOKS.append(new_book)
    save_books(BOOKS)
    return {"message": "Book added successfully"}

@app.put('/books/update_book')
async def update_book(updated_book: Dict[str, Any] = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            save_books(BOOKS)
            return {"message": "Book updated successfully"}
    return {"message": "Book not found"}

@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            save_books(BOOKS)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}
