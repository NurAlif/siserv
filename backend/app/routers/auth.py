from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import database, schemas, models, security

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Handles user registration with whitelist validation.
    - Hashes the password.
    - Checks for existing user/email/student_id.
    - Validates student_id and email against the StudentWhitelist.
    - Creates a new user in the database.
    """
    # --- NEW: Whitelist Validation ---
    whitelisted_student = db.query(models.StudentWhitelist).filter(models.StudentWhitelist.student_id == user.student_id).first()
    
    if not whitelisted_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID is not approved for registration."
        )

    # Case-insensitive email comparison
    if whitelisted_student.email.lower() != user.email.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided email does not match the one registered for this Student ID."
        )
    # --- END NEW: Whitelist Validation ---

    # Check if a user with the same email or username already exists
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken."
        )

    db_user_studentid = db.query(models.User).filter(models.User.student_id == user.student_id).first()
    if db_user_studentid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID is already registered."
        )

    # Hash the password before storing
    hashed_password = security.get_password_hash(user.password)
    
    # Create a new user instance and save to the database
    new_user = models.User(
        username=user.username,
        email=user.email,
        realname=user.realname,
        student_id=user.student_id,
        group=user.group,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Refresh the instance to get the new ID and created_at

    return new_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Handles user login.
    - Verifies username/student_id and password.
    - Returns a JWT access token on success.
    """
    # Find the user by their username OR student_id
    user = db.query(models.User).filter(
        or_(
            models.User.username == form_data.username,
            models.User.student_id == form_data.username
        )
    ).first()

    # If user doesn't exist or password doesn't match, raise an error
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the access token
    access_token = security.create_access_token(
        data={"user_id": user.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    """
    Fetches the profile for the currently logged-in user.
    Requires a valid JWT in the Authorization header.
    """
    return current_user
