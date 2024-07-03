from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models, routes
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes.router, tags=["MortgageCalculator"], prefix="/api/v1")


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}
