from fastapi import FastAPI
from .database import Base, engine
from .routers import users, auth as auth_router

# For quick start; in real projects prefer Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + PostgreSQL JWT Example")

app.include_router(auth_router.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"status": "ok"}
