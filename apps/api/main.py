import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database.redis_client import redis_client
from app.services.router import graphql_router, graphql_app

app = FastAPI(title="TFA")
app.include_router(graphql_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.add_route("/graphql", graphql_app)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup():
    await redis_client.connect()

@app.on_event("shutdown")
async def shutdown():
    await redis_client.disconnect()


if __name__ == "__main__":
    uvicorn.run(app)
