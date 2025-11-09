import os
import stripe
from dotenv import load_dotenv
from financials.stripe.crud.store_account_id import update_owner_stripe_account, get_owner_stripe_account
from property_management.rent.rental_management import get_tenants_rent_info
from financials.stripe.crud.store_account_id import get_owner_stripe_account_with_prop_id, get_single_tenant_rent_info



load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET')



async def setup_tenant_payment(prop_id, tenant_id):

    rent_cost = await get_tenants_rent_info(prop_id, tenant_id)
    owner_stripe_account = await get_owner_stripe_account_with_prop_id(prop_id)
    prod_data = await get_single_tenant_rent_info(tenant_id)
    build_product_data = f"{prod_data.get('fname')} {prod_data.get('lname')} - {prod_data.get('address')}"
    tenant_rent = int(float(rent_cost) * 100)

    try:
        session = stripe.checkout.Session.create(
        line_items=[
            {
            "price_data": {
                "currency": "usd",
                "product_data": {"name": build_product_data},
                "unit_amount": tenant_rent,
            },
            "quantity": 1,
            },
        ],
        payment_intent_data={
            "application_fee_amount": int(tenant_rent * 0.025),
            "transfer_data": {"destination": owner_stripe_account.get('account')},
        },
        mode="payment",
        ui_mode="embedded",
        return_url="http://localhost:3000/rent-view",
        )
            
        return {"client_secret": session.client_secret, 'payment_email':owner_stripe_account.get('email')}
    except stripe.error.StripeError as e:
        raise e
    


async def get_etransfer_email(prop_id:str):
    owner_stripe_account = await get_owner_stripe_account_with_prop_id(prop_id)
    return owner_stripe_account.get('email')