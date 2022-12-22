from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    #role: int


class UserCreate(UserBase):
    ...
   #password: str


class User(UserBase):
    id: int
    is_active: bool
    password: str

    class Config:
        orm_mode = True
