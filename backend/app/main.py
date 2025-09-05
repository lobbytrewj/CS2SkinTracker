from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import items

app = FastAPI(title="CS2 Skin Tracker")

app.add_middleware(
   CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the CS2 Skin Tracker API"}