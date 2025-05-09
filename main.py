import time
import asyncio
from whitenoise import WhiteNoise
from fastapi import FastAPI
from dependencies.firebase import firebase_initializer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers.user_access.admin import router
from routers.dashboard.tenant.ticket_route import ticket_router
from routers.dashboard.owner.update_tickets import mngm_ticket_router
from routers.dashboard.owner.reopen_ticket import reopen_ticket_router
from routers.cloud_services.firebase import firebase
from routers.dashboard.owner.leave_comments import comment_router
from dependencies.redis_client import RedisClient



@asynccontextmanager
async def lifespan(app:FastAPI):
    redis_client=RedisClient()
    await redis_client.redis_client()
    await firebase_initializer(app)
    yield
    await redis_client.redis_client_close()
    pass

app = FastAPI(lifespan=lifespan)


# CORS middleware (to allow specific origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 
                   "https://www.peachstreet.io", 
                   "https://peachstreet.io/", 
                   "https://www.peachstreet.io/",
                   "http://localhost:3000/"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],
    allow_headers=["Content-Type", "Authorization", "*"],
)


app.include_router(router)
app.include_router(ticket_router)
app.include_router(mngm_ticket_router)
app.include_router(reopen_ticket_router)
app.include_router(firebase)
app.include_router(comment_router)