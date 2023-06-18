app = FastAPI()
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


if __name__ == "__main__":
    uvicorn.run(app)
