from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from .. database import get_db


router = APIRouter(
    prefix="/course",
    tags=["Course"]
)

@router.post("/", response_model=schemas.CourseResponse)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # this is the same as: new_course = models.Course(name=course.name, instructor=course.instructor, duration=course.duration, website=course.website)
    new_course= models.Course(**course.model_dump()) 
    new_course.website = str(new_course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.get("/", response_model=List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@router.get("/{id}", response_model=schemas.CourseResponse)
def get_courses(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    return course

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_courses(id: int, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.CourseResponse)
def update_course(id: int, updated_course: schemas.CourseCreate, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    data = updated_course.model_dump() # convert pydantic model to dictionary
    data["website"] = str(data["website"])
    course_query.update(data, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return course

