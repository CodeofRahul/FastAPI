from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

# GET Method

@app.get('/')
async def read_root():
    # return {"Hello World!"}
    return {"message":"Hello World!"}

# endpoint with path parameter
# @app.get('/greet/{name}')
# async def greet_name(name:str) -> dict:
#     return {"message": f"Hello {name}"}

# endpoint with query parameter
@app.get('/greet/{name}')
async def greet_name_age(name:str, age:int) -> dict:
    return {"message": f"Hello {name}", "age":age}


# endpoint with optional parameter
@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}


# POST Method

class BookCreateModel(BaseModel):
    title : str
    author : str

@app.post('/create_book')
async def create_book(book_data:BookCreateModel):
    return {
        "title":book_data.title,
        "author": book_data.author
    }


@app.get('/get_headers', status_code=500)
async def get_headers(
    accept:str = Header(None),
    content_type: str = Header(None),
    user_agent:str = Header(None),
    host:str = Header(None)
):
    request_headers = {}

    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers