from fastapi import FastAPI
from routes import router
from database import engine, Base



app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Notes API"}
