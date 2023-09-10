import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

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
    ui = ''
    return {"Hello": "World"}


@app.get("/a")
def hya(request: Request, session: Session = Depends(main_session)):
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app)
