from fastapi import FastAPI, HTTPException, status, Response, Depends
import psycopg
from psycopg.rows import dict_row
import time 
# from . import models
from sqlalchemy.orm import Session
from . database import engine, get_db
from . import schemas, models
from typing import List

app = FastAPI()

# create the tables in the database
models.Base.metadata.create_all(bind=engine)

@app.get("/sqlalchemy")
def get_courses(db: Session = Depends(get_db)):
    # return db.query(models.Course).all()
    return {"status": "ok"}


while True:
    try:
        conn = psycopg.connect(
            "postgresql://postgres:postgres@localhost/fastapi-sample-app",
            row_factory=dict_row
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection failed, retrying...")
        print("Error: ", error)
        time.sleep(2)




@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "ok"}




# @app.post("/add_course")
# async def create_course(course: Course):
#     # insert the course into the database
#     cursor.execute(
#     """
#     INSERT INTO course (name, instructor, duration, website)
#     VALUES (%s, %s, %s, %s)
#     RETURNING *
#     """,
#     (course.name, course.instructor, course.duration, str(course.website))
#     )
#     # # fetch the new course from the database
#     new_course = cursor.fetchone()
#     # commit the changes to the database before exiting this this data was save into memory
#     conn.commit()
#     return {"data:": new_course}



@app.post("/course", response_model=schemas.CourseResponse)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # this is the same as: new_course = models.Course(name=course.name, instructor=course.instructor, duration=course.duration, website=course.website)
    new_course= models.Course(**course.model_dump()) 
    new_course.website = str(new_course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


# @app.get("/course-list")
# def get_courses():
#     cursor.execute("SELECT * FROM course")
#     data = cursor.fetchall()
#     return {"data":data}


@app.get("/courses", response_model=List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses

# @app.get("/course/{id}")
# def get_courses(id: int):
#     cursor.execute(""" SELECT * FROM course WHERE id = %s """, (id,))
#     data = cursor.fetchone()
#     if not data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
#     return {"data":data}

@app.get("/course/{id}", response_model=schemas.CourseResponse)
def get_courses(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    return course

# @app.delete("/course/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_courses(id: int):

#     cursor.execute(""" DELETE FROM course WHERE id = %s returning * """, (id,))
#     deleted_data = cursor.fetchone()
#     conn.commit()

#     if deleted_data == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
#     return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/delete_course/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_courses(id: int, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/course/{id}")
# async def update_course(id: int, course: Course):
#     # insert the course into the database
#     cursor.execute(
#     """
#     UPDATE course SET  name = %s, instructor = %s, duration = %s, website = %s WHERE id = %s
#     RETURNING *
#     """,
#     (course.name, course.instructor, course.duration, str(course.website), id)
#     )
#     # # fetch the new course from the database
#     updated_course = cursor.fetchone()
#     # commit the changes to the database before exiting this this data was save into memory
#     conn.commit()
#     if not updated_course:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
#     return {"data:": updated_course}


# @app.put("/update_course/{id}", response_model=schemas.CourseResponse)
# def update_course(id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
#     course_query = db.query(models.Course).filter(models.Course.id == id)
#     if not course_query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
#     course_query.update({
#         "name": course.name,
#         "instructor": course.instructor,
#         "duration": course.duration,
#         "website": str(course.website)
#     })
#     db.commit()
#     return {"data": course_query.first()}


@app.put("/course/{id}", response_model=schemas.CourseResponse)
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




# @app.put("/update_course/{id}")
# def update_course(id: int, course: Course, db: Session = Depends(get_db)):
#     course_query = db.query(models.Course).filter(models.Course.id == id)
#     data = course_query.first()
#     if not data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Course not found with id: {id}")
    
#     update_data = course.model_dump()
#     update_data["website"] = str(update_data["website"])
#     course_query.update(update_data, synchronize_session=False)
#     db.commit()
#     db.refresh(course)
#     return {"data": course}


@app.get("/sqlalchemy")
def get_courses(db: Session = Depends(get_db)):
    # return db.query(models.Course).all()
    return {"status": "ok"}

