from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.database.models import AuthUser
from src.schemas import UserModel, UserResponse
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix='/users', tags=["users"])

# @router.get("/", response_model=List[UserResponse], description='No more than 1 requests per 3 minute',
#             dependencies=[Depends(RateLimiter(times=1, seconds=180))])
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
#                      current_user: AuthUser = Depends(auth_service.get_current_user)):
#     users = await repository_users.get_users(skip, limit, current_user, db)
#     return users



@router.get("/all", response_model=List[UserResponse], description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: AuthUser = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users(skip, limit, db, current_user)
    return users


@router.get("/find/{some_info}", response_model=List[UserResponse], description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def find_users_by_some_info(some_info: str, db: Session = Depends(get_db),
                                  current_user: AuthUser = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users_by_some_info(some_info, db, current_user)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users


@router.get("/birthday/{days}", response_model=List[UserResponse], description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def find_birthday_per_week(days: int, db: Session = Depends(get_db),
                                 current_user: AuthUser = Depends(auth_service.get_current_user)):
    users = await repository_users.get_birthday_per_week(days, db, current_user)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return users


@router.get("/{user_id}", response_model=UserResponse, description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def read_user(user_id: int, db: Session = Depends(get_db),
                    current_user: AuthUser = Depends(auth_service.get_current_user)):
    user = await repository_users.get_user(user_id, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))], status_code=status.HTTP_201_CREATED)
async def create_user(body: UserModel, db: Session = Depends(get_db),
                      current_user: AuthUser = Depends(auth_service.get_current_user)):
    return await repository_users.create_user(body, db, current_user)


@router.put("/put/{user_id}", response_model=UserResponse, description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def update_user(body: UserModel, user_id: int, db: Session = Depends(get_db),
                      current_user: AuthUser = Depends(auth_service.get_current_user)):
    user = await repository_users.update_user(user_id, body, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/remove/{user_id}", response_model=UserResponse, description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def remove_user(user_id: int, db: Session = Depends(get_db),
                      current_user: AuthUser = Depends(auth_service.get_current_user)):
    user = await repository_users.remove_user(user_id, db, current_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user