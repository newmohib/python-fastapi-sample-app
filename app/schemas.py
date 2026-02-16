from pydantic import BaseModel, HttpUrl, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# define request body schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseResponse(CourseCreate):
    # return the data as a dictionary, define how the response is going to be returned
    model_config = ConfigDict(from_attributes=True)
    
    id: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
     # return the data as a dictionary, define how the response is going to be returned
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at:datetime



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None