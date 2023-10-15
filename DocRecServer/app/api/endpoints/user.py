"""
Модуль API user.
"""
import typing
import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy.orm import joinedload
from fastapi import Depends, APIRouter, status

from app import schemas, models, db
from app.api import helpers, details


router = APIRouter()


@router.post("", response_model=int)
async def create_user(
        data: schemas.UserCreate,
        session: db.AsyncSession = Depends(db.get_session)
):
    """
    API создания пользователя.
    """
    user_exists = await session.scalar(sa.select(sa.select(models.User).where(
        models.User.telegram_id == data.telegram_id
    ).exists()))
    if user_exists:
        helpers.abort(code=status.HTTP_400_BAD_REQUEST, detail=details.USER_ALREADY_EXISTS)

    user = models.User(telegram_id=data.telegram_id)
    session.add(user)
    try:
        await session.commit()
    except sa.exc.DBAPIError as e:
        await session.rollback()

        helpers.abort(status.HTTP_400_BAD_REQUEST, detail=helpers.error_detail(e))

    return user.id


@router.get("/{telegram_id}", response_model=schemas.UserInDb)
async def read_user(
        telegram_id: str,
        session: db.AsyncSession = Depends(db.get_session)
):
    """
    API получения списка всех пользователей
    """
    user = await helpers.get_user(session=session, telegram_id=telegram_id, load_target_coin=True)

    return user


@router.get("", response_model=typing.List[schemas.UserInDb])
async def read_users(session: db.AsyncSession = Depends(db.get_session)):
    """
    API получения списка всех пользователей
    """
    users = (await session.scalars(sa.select(models.User).options(joinedload(models.User.target_coin)))).all()

    return users


@router.delete("/{telegram_id}", response_model=schemas.Status)
async def delete_user(
        telegram_id: str,
        session: db.AsyncSession = Depends(db.get_session)
):
    """
    API удаления пользователя.
    """
    user = await helpers.get_user(session=session, telegram_id=telegram_id)

    try:
        await session.delete(user)
        await session.commit()
    except sa.exc.DBAPIError as e:
        await session.rollback()

        helpers.abort(code=status.HTTP_400_BAD_REQUEST, detail=helpers.error_detail(e))

    return schemas.Status(status='success')
