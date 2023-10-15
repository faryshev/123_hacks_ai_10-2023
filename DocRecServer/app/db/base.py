"""
Дополнительный модуль base.py.
"""
import re

import sqlalchemy.orm as sa_orm


OriginalBase = sa_orm.declarative_base()


class Base(OriginalBase):
    __abstract__ = True
    __allow_unmapped__ = True

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @sa_orm.declared_attr
    def __tablename__(self) -> sa_orm.Mapped[str]:
        name = self.__name__
        words = re.findall('[A-Z][^A-Z]*', name)
        if words and len(words) > 1:
            words = [word.lower() for word in words]
            name = '_'.join(words)
        else:
            name = name.lower()
        return name
