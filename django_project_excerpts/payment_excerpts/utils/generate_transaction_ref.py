import random
from datetime import datetime
from .constants import PAYOUT_REF_SPLITTER
from .payment_enums import PAYOUT_ACTION
from rest_framework.exceptions import ValidationError


"""
This is useful in generating transaction refs for payouts whether with fincra or paystack
so that the reference is predictable and can be processed easily when the webhook comes in
The splitter string is defined in the constant file so it can be reused in the webhook to split the ref string
The action can then easily be gotten and used to decide what method in the corresponding mixin to call
"""
def generate_payout_ref(username, payout_channel, action):
    if action not in PAYOUT_ACTION.values:
        raise ValidationError('Invalid payout action')
    return f'{action}{PAYOUT_REF_SPLITTER}{username}__{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}__{random.randint(1000,8000000)}__{payout_channel}'
