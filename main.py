from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_access.admin import router
from routers.dashboard.tenant.ticket_route import ticket_router
from routers.dashboard.owner.update_tickets import mngm_ticket_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://helixpropertymanagement-718e761927a1.herokuapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],  # Ensure OPTIONS is allowed
    allow_headers=["Content-Type", "Authorization", "*"],  # Allow headers
)

app.include_router(router)
app.include_router(ticket_router)
app.include_router(mngm_ticket_router)
