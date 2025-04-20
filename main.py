from unittest.util import _MAX_LENGTH
from fastapi import FastAPI, Path, Query
from enum import Enum
from typing import Union
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/Home")
def read_root():
    return {"This is Home endpoint!"}


@app.get("/item/{Item}")
def paht_func(Item):
    var_name = {"path variable": Item}
    return var_name


# create an endpoint that accepts a query parameter 
@app.get("/query/")
def query_func(name: str, roll_no: int):
    var_name = {"name": name, "roll_no": roll_no}
    return query_func

# create an endpoint that accepts a query parameter with default value
@app.get("bydefault")
def with_default(name: str, roll_id: Union[int, None]=None):
    var_name = {"name": name, "roll_id": roll_id}
    return var_name

# Create an end poind that give the option to choose from drop-down list
class Choice_Name(str, Enum):
    one = "one"
    two = "two"
    three = "three"

# create an endpoint where we can choose from the drop-down list
@app.get("/models/{model_name}")
async def get_model(model_name: Choice_Name):
    return model_name


