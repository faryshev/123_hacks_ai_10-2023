"""
Базовый модуль схем.
"""
import datetime

from pydantic import BaseModel


class APIBase(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


def valid_time(value: str) -> datetime.time:
    """Функция переводит строчный формат времени в тип time.

    :param value: Время в строчном формате.

    :return: Время в формате time.
    """
    return datetime.datetime.strptime(value, '%H:%M').time() if value else value
