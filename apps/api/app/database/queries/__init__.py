from typing import Type, Optional

from sqlalchemy.orm import Session, Query

from app.database.base_class import DbBaseModel


class BaseQueries:
    def __init__(self, session: Session):
        self.session = session

    def get_one_or_none_by_id(self, model_class: Type[DbBaseModel], object_id: int) -> Optional[Type[DbBaseModel]]:
        obj = self.session.query(model_class).filter(model_class.id == object_id).one_or_none()

        return obj

    def get_query_with_pagination(self, query: Query, page: int, per_page: int) -> Query:
        query = query.limit(per_page).offset((page - 1) * per_page)

        return query
