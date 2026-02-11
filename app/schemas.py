from pydantic import BaseModel, HttpUrl

# define request body schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseResponse(CourseCreate):
    id: int

    # define how the response is going to be returned
    #orm_mode = True: return the data as a dictionary
    class Config:
        orm_mode = True


