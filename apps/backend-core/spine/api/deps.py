from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from spine.db.engine import get_db
from spine.db.engine import get_db
from spine.db.models import DBUser

# In a real app, use settings.SECRET_KEY
SECRET_KEY = "SECRET_KEY_GOES_HERE" 
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Check if it's our fake token for dev
        if token.startswith("fake-jwt-token-"):
            username = token.replace("fake-jwt-token-", "")
        else:
            # Real JWT Decode (Future)
            # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # username: str = payload.get("sub")
            raise credentials_exception
            
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[DBUser, Depends(get_current_user)]):
    # In future, check current_user.disabled
    return current_user
