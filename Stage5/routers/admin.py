from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel

from database import get_session
from models import User
from auth_utils import get_current_user
from schemas import UserResponse

router = APIRouter()


class RoleUpdateRequest(BaseModel):
    role: str


def require_admin(
    current_user_email: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == current_user_email)
    ).first()

    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user


@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    users = session.exec(select(User)).all()
    return [
        UserResponse(email=user.email, role=user.role)
        for user in users
    ]


@router.patch("/users/{email}/role", response_model=UserResponse)
def update_user_role(
    email: str,
    request: RoleUpdateRequest,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.role = request.role
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(email=user.email, role=user.role)


@router.delete("/users/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    email: str,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    session.delete(user)
    session.commit()