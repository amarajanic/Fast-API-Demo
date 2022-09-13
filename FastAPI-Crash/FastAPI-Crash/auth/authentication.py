from fastapi import APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from auth import oauth2
from db.db_setup import get_db
from fastapi import Depends
from db.models.user import User
from hash import Hash

router = APIRouter(
    tags=['authentication']
)

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
   #if not Hash.verify(user.password, request.password):
    #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    #access_token = oauth2.create_access_token(data={'sub': user.username})
    access_token = oauth2.create_access_token(data={'sub': user.email})



    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
       # 'username': user.username
    }

