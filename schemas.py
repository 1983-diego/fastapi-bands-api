from datetime import date
from enum import Enum
from pydantic import BaseModel, validator

class GenreURLChoices(Enum):
    ROCK ='rock'
    ELETRONIC = 'electronic'
    METAL = 'metal'
    POP = 'pop'

class GenreChoices(Enum):
    ROCK ='Rock'
    ELETRONIC = 'Electronic'
    METAL = 'Metal'
    POP = 'Pop'

class Album(BaseModel):
    title: str
    release_date: date

class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []

class BandCreate(BandBase):
     @validator('genre', pre=True)
     def title_case_genre(cls, value):
         return value.title()

class BandWithID(BandBase):
    id: int