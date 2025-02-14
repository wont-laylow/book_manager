from fastapi import FastAPI
from app.routers import books

app = FastAPI()

app.include_router(books.router)

@app.get("/")
def home():
    return {"message": "welcome to the Bookstore"}