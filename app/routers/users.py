from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserRead,
    UserLogin,
    Token,
    UserProfileUpdate,
    PasswordChange,
    UserProfileResponse,
)
from app.utils import hash_password, verify_password
from app.utils.auth import create_access_token, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if email already exists
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    db_user_username = db.query(User).filter(User.username == user.username).first()
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pwd = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password_hash=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user and return a JWT token.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Retrieve the currently authenticated user's profile.
    """
    return current_user


@router.put("/me", response_model=UserProfileResponse)
def update_current_user(
    update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update profile information (username/email) for the authenticated user.
    Returns a refreshed token when the username changes.
    """
    if update.username and update.username != current_user.username:
        exists = db.query(User).filter(User.username == update.username).first()
        if exists:
            raise HTTPException(status_code=400, detail="Username already taken")

    if update.email and update.email != current_user.email:
        exists = db.query(User).filter(User.email == update.email).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")

    if update.username:
        current_user.username = update.username
    if update.email:
        current_user.email = update.email

    db.commit()
    db.refresh(current_user)

    # Refresh token if username changed
    new_token = None
    if update.username:
        new_token = create_access_token(data={"sub": current_user.username})

    return {
        "user": current_user,
        "access_token": new_token,
        "token_type": "bearer"
    }


@router.post("/change-password")
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change password for the authenticated user after verifying current password.
    """
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
