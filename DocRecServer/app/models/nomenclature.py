"""
Модуль модели номенклатуры компании
"""
import typing

import sqlalchemy as sa
import sqlalchemy.orm

from app import db

if typing.TYPE_CHECKING:
    pass


import sqlalchemy as sa

class Nomenclature(db.Base):
    """Модель таблицы номенклатуры.

    :id: Уникальный идентификатор номенклатуры.
    :name: Наименование номенклатуры.
    :type: Тип номенклатуры.
    :measurement_id: Внешний ключ на таблицу измерений.

    """
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String)
    measurement_id = sa.Column(sa.Integer, sa.ForeignKey('measurement.id'), nullable=False)

    def __str__(self):
        return f'Nomenclature #{self.id}'

    def __repr__(self):
        return f'Nomenclature #{self.id}'
    
    measurement_id: "Measurement" = sa.orm.relationship(
        'Measurement',
        lazy='raise_on_sql',
        foreign_keys=[measurement_id],
        viewonly=True,
        uselist=False
    )
    
    
class Measurement(db.Base):
    """Модель таблицы монет.

    :id: Уникальный идентификатор

    :name: Имя 
    """
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)

    name = sa.Column(sa.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'Measurement id: {self.id}'