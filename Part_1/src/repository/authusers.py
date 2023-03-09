from sqlalchemy.orm import Session

from src.database.models import AuthUser
from src.schemas import AuthUserModel

from libgravatar import Gravatar


async def get_authuser_by_email(email: str, db: Session) -> AuthUser:
    return db.query(AuthUser).filter(AuthUser.email == email).first()


async def create_authuser(body: AuthUserModel, db: Session) -> AuthUser:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = AuthUser(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: AuthUser, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_authuser_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> AuthUser:
    user = await get_authuser_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
