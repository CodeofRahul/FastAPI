from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel
from typing import List

book_router = APIRouter()


# Define an API endpoint to retrieve all books.
# The path is '/' and the HTTP method is GET.
# 'response_model=List[Book]' specifies that the response will be a list of Book objects.
@book_router.get('/', response_model=List[Book])
async def get_all_books():
    # This function simply returns the 'books' list.
    return books

# Define an API endpoint to create a new book.
# The path is '/books' and the HTTP method is POST.
# 'status_code=status.HTTP_201_CREATED' sets the HTTP status code for a successful creation.
# 'book_data: Book' indicates that the request body should be a JSON object that can be validated against the Book Pydantic model.
# '-> dict' specifies that the function will return a dictionary (which FastAPI will automatically convert to JSON).
@book_router.post('/', status_code=status.HTTP_201_CREATED)
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
@book_router.get('/{book_id}')
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
@book_router.patch('/{book_id}')
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
@book_router.delete('/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
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
