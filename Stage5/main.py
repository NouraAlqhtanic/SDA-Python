from fastapi import FastAPI

from database import create_db
from models import User
from routers import auth
from routers import auth, admin, evaluate

app = FastAPI(title="Resume Evaluator API - Stage 4")


@app.on_event("startup")
def on_startup():
    create_db()


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
)

app.include_router(
    evaluate.router,
    prefix="/evaluate",
    tags=["evaluate"]
)


@app.get("/")
def root():
    return {"message": "Stage 4 API is running"}