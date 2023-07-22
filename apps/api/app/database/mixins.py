from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime, func

from app.database.base_class import DbBaseModel


class CreatedUpdatedDeletedMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    def delete(self):
        self.deleted_at = datetime.now(timezone.utc)


def create_linking_table(
        left: type[DbBaseModel],
        right: type[DbBaseModel],
        basemodel: type[DbBaseModel] = DbBaseModel,
        ondelete: str | None = None,
        table_name: str | None = None
) -> Table:

    left_column_name: str = f"{left.__name__.lower()}_{left.id.name}"
    right_column_name: str = f"{right.__name__.lower()}_{right.id.name}"

    table = Table(
        table_name or f"{left.__name__.lower()}_{right.__name__.lower()}",
        basemodel.metadata,
        Column(
            left_column_name,
            Integer,
            ForeignKey(left_column_name.replace("_", "."), ondelete=ondelete),
            nullable=False
        ),
        Column(
            right_column_name,
            Integer,
            ForeignKey(right_column_name.replace("_", "."), ondelete=ondelete),
            nullable=False
        )
    )

    return table
