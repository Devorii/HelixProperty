import os
import stripe
from dotenv import load_dotenv
load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET')


def delete_stripe_account():
    '''
    Removes the user's account with Stripe account id.

    :params:str landlord_stripe_account   
    :return delete_account
    '''

    try: 
        stripe.Account.delete('acct_1SIys156R3beJWvR')
        print('account deleted')
        return dict(status=200, message='Account deleted.') 
    except stripe.StripeError as e:
        raise e
    
delete_stripe_account()