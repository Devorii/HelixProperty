import os
import stripe
from dotenv import load_dotenv
from financials.stripe.crud.store_account_id import update_owner_stripe_account, get_owner_stripe_account



load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET')



async def setup_tenant_payment():
    pass

# Store the account.id in the database if the landlord needs to continue onboarding or access their dashboard.
async def setup_landlord_account(uid:int, email:str, backgroundtask) -> dict:
    '''
    Takes in users landlords email and creates a stripe account 
    For them. 

    :params:str email
    :return:dict 
    '''

    try: 
        account = stripe.Account.create(
        type="express",
        country="CA",
        email=email,
        business_type="individual",
        individual={
        "first_name": "REQUIRED_LANDLORD_FIRST_NAME",
        "last_name": "REQUIRED_LANDLORD_LAST_NAME",
        "email": email,
        "dob": {
            "day": 1,
            "month": 1,
            "year": 1980
        },

        "verification": {
            "document": {}
        }
    },
        business_profile={
            "mcc": "6513",
            "product_description": "Collecting residential rent payments for tenants via Peach Street platform",
            "url": "https://www.peachstreet.io",
            },
        capabilities={
            "transfers": {"requested": True} 
        }
        )

        account_link=stripe.AccountLink.create(
            account=account.id, 
            refresh_url="https://www.peachstreet.io",
            return_url="https://www.peachstreet.io",
            type="account_onboarding"
        )

        backgroundtask.add_task(update_owner_stripe_account, uid, account.id)
        return dict(status=200, account_id=account.id, onboarding_url=account_link.url)
    except stripe.StripeError as e:
        raise e



async def create_express_dashboard(uid:int):
    '''
    Creates temporary link for the landlord to view their accounts. 

    :params:str landlord_account_id
    :return:dict url_link
    '''
    landlord_stripe_account_id= await get_owner_stripe_account(uid)
    try:
        balance = stripe.Balance.retrieve(stripe_account=landlord_stripe_account_id)
        payouts = stripe.Payout.list( stripe_account=landlord_stripe_account_id, limit=1)
        next_payout = payouts.data[0] if payouts.data else None


        account_link=stripe.Account.create_login_link(landlord_stripe_account_id)
        return dict(status=200, 
                    account_url=account_link.url, 
                    balance=balance,
                    next_payout=next_payout)
    except stripe.StripeError as e:
        raise e

async def create_express_session(uid:int):
    '''
    Creates temporary link for the landlord to view their accounts. 

    :params:str landlord_account_id
    :return:dict url_link
    '''
    landlord_stripe_account_id= await get_owner_stripe_account(uid)
    try:
        account_session = stripe.AccountSession.create(
          account=landlord_stripe_account_id,
          components={
            "payments": {
              "enabled": True,
              "features": {
                "refund_management": True,
                "dispute_management": True,
                "capture_payments": True
              }
            },
          },
        )
        return {'client_secret': account_session.client_secret}
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account session: ', e)
        return dict(error=str(e)), 500


async def delete_stripe_account(uid:int):
    '''
    Removes the user's account with Stripe account id.

    :params:str landlord_stripe_account   
    :return delete_account
    '''
    landlord_stripe_account_id=get_owner_stripe_account(uid)
    try: 
        stripe.Account.delete(landlord_stripe_account_id)
        return dict(status=200, message='Account deleted.') 
    except stripe.StripeError as e:
        raise e