from fastapi import FastAPI
from routers import auth
from routers import auth, evaluate
app = FastAPI(title="Resume Evaluator API")

app.include_router(
    evaluate.router,
    tags=["evaluate"]
)
@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)