# app/routers/home.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_home():
    return {"message": "Welcome to the API!"}
