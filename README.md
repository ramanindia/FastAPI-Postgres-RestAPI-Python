# FastAPI-Postgres-API-Python
A comprehensive backend boilerplate built with FastAPI and PostgreSQL, following best practices for scalable REST API development in Python. This template is ideal for building modern, production-ready APIs with authentication, async database operations, and clean architecture.

## Environment Setup
Create and configure your .env file:

DATABASE_URL=postgresql+psycopg://postgres:CEROVtn2025@34.14.200.210:5432/mydb

SECRET_KEY=CHANGE_ME_SUPER_SECRET

ACCESS_TOKEN_EXPIRE_MINUTES=1440

## Virtual Environment Setup

python -m venv .venv

source .venv/bin/activate

## Install Dependencies
pip install -r requirements.txt

## Run the Application

uvicorn app.main:app --reload

Your app will be available at:

http://127.0.0.1:8000/

 ## API Documentation
Access automatically generated API docs here:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

