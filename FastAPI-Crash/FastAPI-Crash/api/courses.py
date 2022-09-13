import fastapi

from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi import Path

from db.db_setup import get_db
from pydantic_schemas.course import CourseCreate, Course
from api.utils.courses import get_course, get_courses, create_course

router = fastapi.APIRouter()


@router.get("/courses", tags={"course"})
async def read_courses(db: Session = Depends(get_db)) -> list:
    courses = get_courses(db)
    return courses


# @router.post("/courses")
# async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
#         created_course = create_course(db, course)
#         if created_course:
#             return created_course
#         else:
#             raise HTTPException(status_code=405, detail="Course not created")

@router.post("/courses", response_model=Course, tags={"course"})
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)

@router.get("/courses/{id}", tags={"course"})
async def read_course(id:int, db: Session = Depends(get_db)):
    course = get_course(db, id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    else:
        return course
