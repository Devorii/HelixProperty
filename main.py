from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import admin

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://helixpropertymanagement-718e761927a1.herokuapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin.router)
