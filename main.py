from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.endpoints.routes import routers
import uvicorn

app = FastAPI()
app.include_router(routers)

origins = [
    "http://localhost:3000",
    "https://travel-right-fe.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI studio called ATLAS. Named after that famous giant of the Olympus ⚡ in Greek mythology."}
