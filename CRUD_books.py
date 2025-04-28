from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI application
app = FastAPI()

# In-memory list to store book data. In a real application, this would likely be a database.
books = [


    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "o'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English"
    },
    {
        "id": 2,
        "title": "Django By Example",
        "author": "Antonio Mele",
        "publisher": "Packt Publishing Ltd",
        "published_date": "2022-01-19",
        "page_count": 1023,
        "language": "English"
    },
    {
        "id": 3,
        "title": "The web socket handbook",
        "author": "Alex Diaconu",
        "publisher": "Xinyu Wang",
        "published_date": "2021-01-01",
        "page_count": 3677,
        "language": "English"
    },
    {
        "id": 4,
        "title": "Head first Javascript",
        "author": "Hellen Smith",
        "publisher": "Oreilly Media",
        "published_date": "2021-01-01",
        "page_count": 540,
        "language": "English"
    },
    {
        "id": 5,
        "title": "Algorithm and Data Structures In Python",
        "author": "Kent Lee",
        "publisher": "Springer, Inc",
        "published_date": "2026-01-01",
        "page_count": 9282,
        "language": "English"
    },
    {
        "id": 6,
        "title": "Head first HTML5 Programming",
        "author": "Eric T Freeman",
        "publisher": "O'Reilly Media",
        "published_date": "2011-21-01",
        "page_count": 3006,
        "language": "English"
    },
]

# Pydantic model for representing a Book object.
# This helps in data validation and serialization/deserialization.
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

# Pydantic model for updating a Book object.
# It includes all the fields of a Book, but they are optional for updating.
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

# Define an API endpoint to retrieve all books.
# The path is '/books' and the HTTP method is GET.
# 'response_model=List[Book]' specifies that the response will be a list of Book objects.
@app.get('/books', response_model=List[Book])
async def get_all_books():
    # This function simply returns the 'books' list.
    return books

# Define an API endpoint to create a new book.
# The path is '/books' and the HTTP method is POST.
# 'status_code=status.HTTP_201_CREATED' sets the HTTP status code for a successful creation.
# 'book_data: Book' indicates that the request body should be a JSON object that can be validated against the Book Pydantic model.
# '-> dict' specifies that the function will return a dictionary (which FastAPI will automatically convert to JSON).
@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict:
    # Convert the Pydantic Book object to a dictionary.
    new_book = book_data.model_dump()
    # Add the new book to our in-memory list.
    books.append(new_book)
    # Return the newly created book.
    return new_book

# Define an API endpoint to retrieve a specific book by its ID.
# The path is '/book/{book_id}' where '{book_id}' is a path parameter that will be an integer.
# The HTTP method is GET.
# 'book_id: int' specifies that the 'book_id' path parameter should be an integer.
# '-> dict' specifies that the function will return a dictionary.
@app.get('/book/{book_id}')
async def get_book(book_id:int) -> dict:
    # Iterate through the 'books' list.
    for book in books:
        # Check if the 'id' of the current book matches the requested 'book_id'.
        if book['id'] == book_id:
            # If a match is found, return the book.
            return book
        # If the loop finishes without finding a matching book, raise an HTTPException with a 404 Not Found status code and a detail message.
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

# Define an API endpoint to update an existing book by its ID.
# The path is '/book/{book_id}' where '{book_id}' is a path parameter that will be an integer.
# The HTTP method is PATCH (used for partial updates).
# 'book_id: int' specifies that the 'book_id' path parameter should be an integer.
# 'book_update_data: BookUpdateModel' indicates that the request body should be a JSON object that can be validated against the BookUpdateModel.
# '-> dict' specifies that the function will return a dictionary.
@app.patch('/book/{book_id}')
async def update_book(book_id:int, book_update_data:BookUpdateModel) -> dict:
    # Iterate through the 'books' list.
    for book in books:
        # Check if the 'id' of the current book matches the requested 'book_id'.
        if book['id'] == book_id:
            # Update the fields of the book with the data provided in 'book_update_data'.
            # We are only updating the fields that are present in 'book_update_data'.
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            # Return the updated book.
            return book
        
    # If the loop finishes without finding a matching book, raise an HTTPException with a 404 Not Found status code and a detail message.
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# Define an API endpoint to delete a book by its ID.
# The path is '/book/{book_id}' where '{book_id}' is a path parameter that will be an integer.
# The HTTP method is DELETE.
# 'status_code=status.HTTP_204_NO_CONTENT' sets the HTTP status code for a successful deletion with no response body.
# 'book_id: int' specifies that the 'book_id' path parameter should be an integer.
# '-> dict' specifies that the function will return a dictionary (which will be empty in this case as per HTTP 204).
@app.delete('/book/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    # Iterate through the 'books' list.
    for book in books:
        # Check if the 'id' of the current book matches the requested 'book_id'.
        if book["id"] == book_id:
            # If a match is found, remove the book from the list.
            books.remove(book)
            # Return an empty dictionary, indicating successful deletion with no content.
            return {}
    
    # If the loop finishes without finding a matching book, raise an HTTPException with a 404 Not Found status code and a detail message.
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

