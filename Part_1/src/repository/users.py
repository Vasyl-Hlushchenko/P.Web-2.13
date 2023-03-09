from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session

from src.database.models import User, AuthUser
from src.schemas import UserModel


async def get_users(skip: int, limit: int, db: Session, user: AuthUser) -> List[User]:
    return db.query(User).filter(User.authuser_id == user.id).offset(skip).limit(limit).all()


async def get_user(user_id: int, db: Session, user: AuthUser) -> User:
    return db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()


async def create_user(body: UserModel, db: Session, user: AuthUser) -> User:
    user = User(first_name=body.first_name, 
    second_name=body.second_name, 
    email=body.email, 
    phone=body.phone, 
    birthaday=body.birthaday, 
    description=body.description,
    authuser_id=user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(user_id: int, body: UserModel, db: Session, user: AuthUser) -> User| None:
    usr= db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()
    if usr:
        usr.first_name = body.first_name
        usr.second_name = body.second_name
        usr.email = body.email
        usr.phone = body.phone
        usr.birthaday = body.birthaday
        usr.description = body.description
        usr.authuser_id = user.id
        db.commit()
    return usr


async def remove_user(user_id: int, db: Session, user: AuthUser)  -> User | None:
    user = db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_users_by_some_info(some_info: str, db: Session, user: AuthUser) -> List[User]:
    response = []
    info_by_first_name = db.query(User).filter(and_(User.first_name.like(f'%{some_info}%'), User.authuser_id == user.id)).all()
    if info_by_first_name:
        for n in info_by_first_name:
            response.append(n)
    info_by_second_name = db.query(User).filter(and_(User.second_name.like(f'%{some_info}%'), User.authuser_id == user.id)).all()
    if info_by_second_name:
        for n in info_by_second_name:
            response.append(n)
    info_by_email = db.query(User).filter(and_(User.email.like(f'%{some_info}%'), User.authuser_id == user.id)).all()
    if info_by_email:
        for n in info_by_email:
            response.append(n)
            
    return response


async def get_birthday_per_week(days: int, db: Session, user: AuthUser) -> User:
    response = []
    all_users = db.query(User).filter(User.authuser_id == user.id).all()
    for usr in all_users:
        if timedelta(0) <= ((usr.birthaday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(usr)

    return response

