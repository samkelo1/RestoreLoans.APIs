from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if a user with the same email, ID number, or phone number already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.id_number == user_data.id_number) |
        (User.phone_number == user_data.phone_number)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email, ID number, or phone number already exists."
        )

    # Hash the password before saving it
    hashed_password = AuthService.hash_password(user_data.password)

    # Create a new user instance
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        id_number=user_data.id_number,
        email=user_data.email,
        phone_number=user_data.phone_number,
        gender=user_data.gender,
        password=hashed_password,
        is_active=user_data.is_active
    )

    # Add the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Retrieve the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    # Retrieve all users
    users = db.query(User).all()
    return users