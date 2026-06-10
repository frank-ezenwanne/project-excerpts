from django.conf import settings

"""
NB: Please note that these are generic excerpts from a larger codebase protected by NDA,
hence some code might be left out.
"""

from .payment_enums import PAYOUT_CHANNEL, PAYIN_MEDIUM


BASE_CURRENCY = 'USD'
LOCAL_CURRENCY = 'NGN'
DEFAULT_BANK_ACC_VERIFIER = PAYOUT_CHANNEL.FINCRA.value
LOCAL_BANK_ACC_VERIFIER = PAYOUT_CHANNEL.PAYSTACK.value
DEFAULT_CURRENCY_FIELDS_SERVICE = PAYOUT_CHANNEL.FINCRA.value
CARD_EXPIRY_REMINDER_DAYS = 60
DEFAULT_PAYOUT_CHANNEL = None

LOCAL_PAYOUT_CHANNEL = PAYOUT_CHANNEL.PAYSTACK.value
OTHER_PAYOUT_CHANNEL = PAYOUT_CHANNEL.FINCRA.value #fallback payout if default and user specified are not available
LOCAL_BANKS_LIST_CHANNEL = PAYOUT_CHANNEL.PAYSTACK.value

payout_channels_with_recipient_ids = [
    PAYOUT_CHANNEL.PAYSTACK.value,
]


PAYOUT_REF_SPLITTER ='---'

WEBHOOK_HEADER_KEYWORD = { 
    PAYOUT_CHANNEL.PAYSTACK.value:'x-paystack-signature',
    PAYIN_MEDIUM.STRIPE.value:'Stripe-Signature',
    PAYOUT_CHANNEL.FINCRA.value:'signature'
}

WEBHOOK_KEY = {
    f'{PAYOUT_CHANNEL.PAYSTACK.value}':settings.PAYSTACK_SECRET_KEY,

    f'{PAYIN_MEDIUM.STRIPE.value}': settings.STRIPE_WEBHOOK_SECRET,
  
    f'{PAYOUT_CHANNEL.FINCRA.value}' : settings.FINCRA_WEBHOOK_SECRET
}


