from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas
from .. database import get_db
from .. import oauth2


router = APIRouter(
    prefix="/course",
    tags=["Course"]
)

@router.post("/", response_model=schemas.CourseResponse)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # this is the same as: new_course = models.Course(name=course.name, instructor=course.instructor, duration=course.duration, website=course.website)
    new_course= models.Course(**course.model_dump(), creator_id=current_user.id) 
    new_course.website = str(new_course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.get("/", response_model=List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 2, skip: int = 0, search:Optional[str] = ""):
    # courses = db.query(models.Course).all()
    courses = db.query(models.Course).filter(models.Course.creator_id == current_user.id).filter(models.Course.name.contains(search)).limit(limit).offset(skip).all()
    return courses


@router.get("/{id}", response_model=schemas.CourseResponse)
def get_courses(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action")
    return course

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_courses(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.CourseResponse)
def update_course(id: int, updated_course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform requested action")
    data = updated_course.model_dump() # convert pydantic model to dictionary
    data["website"] = str(data["website"])
    course_query.update(data, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return course

