# Python
from typing import Optional
from enum import Enum

# pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import Body, FastAPI, Path, Query

"""
    * INSTALL fastAPI
    - pip install fastapi uvicorn
    - uvicorn main:app --reload
"""

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    yellow = "yellow"
    blond = "blonde"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str



class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example = "Luis"
        ),
    last_name: str  = Field(
        ..., 
        min_length=1,
        max_length=50,
        example = "Lopez"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example = "black")
    is_married: Optional[bool] = Field(default=None, example = False)

    # example schema
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Juan",
                "last_name": "Solares",
                "age": 21,
                "hair_color": "blonde",
                "is_married": False
            }
        }



@app.get("/")
def home():

    return {
        "Hello": "juan"
    }

# Request and response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    
    return person


# Validaciones: Query parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person name",
        description="this is the person name. It's between 1 and 50 characters",
        example="Laura"
        ),
    age: Optional[str] = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
):

    return {
        name: name,
        age: age
    }

# Validaciones: Path parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
):

    return {
        person_id: "It exists!"
    }

# Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):

    #results = person.dict()
    #results.update(location.dict())

    return person