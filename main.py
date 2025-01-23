from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_access.admin import router
from routers.dashboard.tenant.ticket_route import ticket_router
from routers.dashboard.owner.update_tickets import mngm_ticket_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development frontend
        "https://helixpropertymanagement-718e761927a1.herokuapp.com"  # Deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow necessary methods
    allow_headers=["Content-Type", "Authorization", "X-Custom-Header"],  # Allow required headers
)

app.include_router(router)
app.include_router(ticket_router)
app.include_router(mngm_ticket_router)
