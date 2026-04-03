from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserResponse, UserUpdate
from app.dependencies import role_required


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to list all registered users."""
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to retrieve details of a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to update user role or status."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to permanently delete a user."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves (optional but recommended)
    if db_user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own admin account")
    
    db.delete(db_user)
    db.commit()
    return None
