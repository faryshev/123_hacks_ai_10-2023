"""
Модуль модели работников
"""
import typing

import sqlalchemy as sa
import sqlalchemy.orm

from app import db

if typing.TYPE_CHECKING:
    pass


class Department(db.Base):
    """Модель таблицы отделов.

    :id: Уникальный идентификатор отдела.
    :name: Наименование отдела.

    """
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)

    employees = sqlalchemy.orm.relationship('Employee', back_populates='department')

    def __str__(self):
        return f'Department #{self.id}'

    def __repr__(self):
        return f'Department #{self.id}'


class Employee(db.Base):
    """Модель таблицы сотрудников.

    :id: Уникальный идентификатор сотрудника.
    :name: Имя сотрудника.
    :position: Должность сотрудника.
    :access_level: Уровень доступа сотрудника.
    :company_id: Внешний ключ на таблицу компаний.
    :department_id: Внешний ключ на таблицу отделов.

    """
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    position = sa.Column(sa.String)
    access_level = sa.Column(sa.String)
    department_id = sa.Column(sa.Integer, sa.ForeignKey('department.id'), nullable=False)

    department = sqlalchemy.orm.relationship('Department', back_populates='employees')

    def __str__(self):
        return f'Employee #{self.id}'

    def __repr__(self):
        return f'Employee #{self.id}'