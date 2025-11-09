from fastapi import APIRouter,Depends
from property_management.reporting_system.view_tickets import view_tickets
from security.access_control.auth.dependencies.session_control import validate_user_account
from financials.stripe.tenants_payments import setup_tenant_payment, get_etransfer_email


tenant_rent_router = APIRouter(
    prefix="/rent",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)

@tenant_rent_router.post('/payments')
async def make_rent_payments(payload:dict, tenant_id:str=Depends(validate_user_account)):
    '''
    Creates stripe intent for tenant to pay their rent.
    '''
    # prop_id, tenant_id

    return await setup_tenant_payment(payload.get('property_id'), tenant_id)



@tenant_rent_router.post('/e-transfer-email')
async def get_rent_email(payload:dict, _:str=Depends(validate_user_account)):
    '''
    Get email for client e-transfer
    '''
    email=await get_etransfer_email(payload.get('property_id'))
    return dict(email=email)