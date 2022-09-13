from importlib import import_module
import fastapi
from fastapi import status
import uvicorn

from typing import List, Optional

from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import async_get_db

from fastapi import Path

from db.db_setup import get_db
from pydantic_schemas.course import Course
from pydantic_schemas.user import UserCreate, User, UserBase
from api.utils.users import get_user, get_users, get_user_by_email, create_user, delete_user, update_user
from api.utils.courses import get_courses_by_user_id
from auth.oauth2 import oauth2_schema
from auth.oauth2 import get_current_user
from custom_log import  log
import time
router = fastapi.APIRouter(
    prefix="/users",
    tags=["users"]


)


@router.get("/",
            response_model=List[User],
            summary="Retrieve all users",
            description="This api call simulates fetching all the users.",
            response_description="The list of all users")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)) -> list:
    # users = get_users(db, skip=skip, limit=limit)
    # return users
    return {
        'data': get_users(db),
        'current_user': current_user
    }


def time_consuming_functionality():
    time.sleep(5)
    return 'ok'


@router.post("/")
async def post_user(user: User, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise  HTTPException(status_code=405, detail="User exists")
    else:
       created_user = create_user(db,user)
       return created_user


@router.patch("/{id}")
async def patch_user(id: int, request: User, db: Session = Depends(get_db)):
    return update_user(db, id, request)




@router.get("/{id}")
async def read_user(response: Response, id:int = Path(..., description="The ID of user you want to retrieve."), db: Session = Depends(get_db)):
    log("MyApi", "Call to get user with id")
    #await time_consuming_functionality()
    user = get_user(db, id)
    if user is None:
    #raise HTTPException(status_code=404, detail="No user with that id")
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_200_OK
        response.set_cookie(key="test", value="test_value_v1")
        return user


# @router.get("/users/{id}") not working
# async def read_user(id:int = Path(..., description="The ID of user you want to retrieve."), db: AsyncSession = Depends(async_get_db)):
#     user = await get_user(db, id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="No user with that id")
#     return user


@router.get("/{id}/courses", response_model=List[Course])
async def read_user_courses(id:int, db: Session = Depends(get_db)):
    courses = get_courses_by_user_id(db=db, user_id=id)
    if courses is None:
        raise HTTPException(status_code=404, detail="There are no courses with that user_id")
    return courses


@router.delete("/{id}")
async def remove_user(id:int, db: Session = Depends(get_db)):
    delete_user(db,id)
    return {"message:", "Success"}








