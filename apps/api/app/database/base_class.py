from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative, declared_attr

db_wide_constraint_naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db_metadata = MetaData(naming_convention=db_wide_constraint_naming_convention)


@as_declarative(metadata=db_metadata)
class DbBaseModel:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
