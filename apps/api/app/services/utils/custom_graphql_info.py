from dataclasses import dataclass
from typing import Any

from fastapi import WebSocket, Request
from graphql import GraphQLResolveInfo
from sqlalchemy.orm import Session


@dataclass
class GraphQLAppContext:
    request: Request = None
    ws: WebSocket = None
    background_tasks: Any = None
    session: Session = None
    authorization: str = None

    user: None = None

    # # necessary because graphene needs context to have this method
    def get(self, key: str):
        return getattr(self, key, None)

    def __getitem__(self, key: str):
        return self.get(key)


class TFAGraphQLResolveInfo(GraphQLResolveInfo):
    context: GraphQLAppContext


def make_context(request: Request):
    session = request.state.db_session
    background_tasks = request.state.background_tasks

    graphql_context = GraphQLAppContext(
        request=request,
        session=session,
        authorization=request.headers.get("Authorization"),
        background_tasks=background_tasks,
    )

    return graphql_context
