from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.routers import users, posts
from app.views import router as views_router
from app import storage
import asyncio

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(users.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(views_router)


@app.on_event("startup")
async def startup_event():
    await storage.load_from_file()
    storage.lock = asyncio.Lock()


@app.on_event("shutdown")
async def shutdown_event():
    await storage.save_to_file()
