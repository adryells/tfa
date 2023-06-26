from fastapi import APIRouter, Request, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from starlette.datastructures import URL
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler

from app.database.session import main_session
from app.services.schema import graphql_schema
from app.services.utils.custom_graphql_info import make_context

graphql_app = GraphQLApp(
    schema=graphql_schema,
    context_value=make_context,
    on_get=make_playground_handler()
)

graphql_router = APIRouter()


@graphql_router.get("/graphql")
async def graphql(request: Request,
                  background_tasks: BackgroundTasks,
                  db_session: Session = Depends(main_session)):
    request.state.db_session = db_session
    request.state.background_tasks = background_tasks
    request._url = URL('/graphql')

    return await graphql_app._get_on_get(request=request) # noqa


@graphql_router.post("/graphql")
async def graphql_post(request: Request,
                       background_tasks: BackgroundTasks,
                       db_session: Session = Depends(main_session)):
    request.state.db_session = db_session
    request.state.background_tasks = background_tasks

    return await graphql_app._handle_http_request(request=request) # noqa
