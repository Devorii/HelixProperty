from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_access.admin import router
from routers.dashboard.tenant.ticket_route import ticket_router
from routers.dashboard.owner.update_tickets import mngm_ticket_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://helixpropertymanagement-718e761927a1.herokuapp.com", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(ticket_router)
app.include_router(mngm_ticket_router)
