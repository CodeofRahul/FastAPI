from pydantic import BaseModel

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