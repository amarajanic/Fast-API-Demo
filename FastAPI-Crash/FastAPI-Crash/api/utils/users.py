from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.user import User
from pydantic_schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# async def get_user(db: AsyncSession, user_id: int):
#     query = select(User).where(User.id == user_id)
#     result = await db.execute(query)
#
#   return result.scalar_one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, id:int, request: User):
    user = db.query(User).filter(User.id == id)
    user.update({
        User.email: request.email,
        User.is_active: request.is_active
    })
    db.commit()
    return 'ok'


def create_user(db: Session, user: UserCreate):
    #fake_hashed_password = user.password + "notreallyhashed"
    #db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db_user = User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id:int):
    user = get_user(db, id)
    db.delete(user)
    db.commit()
