from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from utils.generic_webhook_validator import generic_webhook_validator
from utils.constants import WEBHOOK_HEADER_KEYWORD, WEBHOOK_KEY, PAYOUT_REF_SPLITTER
from utils.payment_enums import PAYOUT_CHANNEL, PAYIN_MEDIUM, ONLINE_PAYREQUEST_CATEGORY, PAYOUT_ACTION
from payment.payin_func import CoinsPurchaseWebhookMixin, MembershipPurchaseWebhookMixin
from admin_panel.payment_func import PayoutWebhookMixin
import stripe
from utils.normalize_booleans import normalize_booleans
from logging import getLogger
logger = getLogger("django_server")



"""
NB: Please note that these are generic excerpts from a larger codebase protected by NDA
hence some mixins imported above are not included in this excerpt.

Below, there are 3 webhook api views pointing to 3 different 3rd party payment gateways
This arrangement helps to easily control and separate webhook logic from the actual processing.
A dedicated routing app was created in the actual django project to help 'keep logic together'

Keeping the logic together stems from understanding how the mixins were structured.
The mixins are Python classes that have predictable method classes e.g the mixin class for 
coins purchase contains methods in this format:

{payment_medium}_{action}_webhook e.g stripe_coins_purchase_webhook, paystack_coins_purchase_webhook,
paystack_membership_purchase_webhook etc, 
So the point is, a webhook mixin for coins purchase will have all accepted payment platforms having methods in
the mixin class. 
But this structure means that the urls which will have either stripe or paystack attached to the url path name,
will route into the same class, so we'll have to separate first according to 3rd party service, and
second according to action, which is cumbersome .

So instead, the webhook api views directly linked to the urls below are in form of 
one for each payment gateway, instead of one for each action. 

This is made possible because of the request_category in the metadata, specifying the action, positioning
the api views below as 'tree trunks' that separate into branches i.e class methods (in the mixin class).

The code below for the pay-in mediums i.e paystack and stripe will validate the webhook
signature and with the request_category extracted from the metadata , look for the corresponding
method in the class with the {payment_medium}_{action}_webhook style.

Generic webhook validators were used for paystack and fincra, but the inbuilt python library 
for stripe was used for stripe webhooks

The payouts with paystack and fincra use transaction reference in place of request_category from metadata
The reference is usually built by an utility function specified in the utils folder in this excerpt.
The utility function uses a splitter string to separate the action fromthe rest of the string.
When the webhook returns, the action is extracted and used to determine the mixin method to be called

"""


class PayStackWebhookRouteView(APIView, CoinsPurchaseWebhookMixin, MembershipPurchaseWebhookMixin, PayoutWebhookMixin):

    request_category_map = {
        ONLINE_PAYREQUEST_CATEGORY.COINS.value:'coins_purchase_webhook',
        ONLINE_PAYREQUEST_CATEGORY.MEMBERSHIP.value:'membership_purchase_webhook'
    }

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            payload = generic_webhook_validator(
                request=request, 
                webhook_key = WEBHOOK_KEY[f'{PAYIN_MEDIUM.PAYSTACK.value}'],
                header_keyword = WEBHOOK_HEADER_KEYWORD[f'{PAYIN_MEDIUM.PAYSTACK.value}']
            )
        except Exception as e:
            logger.error(f"Paystack webhook validation failed: {str(e)}")
            raise e
        
        data = payload.get('data', {})
        method = None
        if data.get('metadata',{}).get('request_category'): #for paystack payins
            request_category = data['metadata'].get('request_category')
            mapped_req_category = self.request_category_map.get(request_category)
            if mapped_req_category:
                method = getattr(self, f"{PAYIN_MEDIUM.PAYSTACK.value}_{self.request_category_map[request_category]}", None)
          
        else: #for paystack payouts
            if data.get('reference'):
                ref = data['reference']
                action = ref.split(PAYOUT_REF_SPLITTER)[0]
                if action in PAYOUT_ACTION.values:
                     method = getattr(self, f"{PAYIN_MEDIUM.PAYSTACK.value}_payout_webhook", None)
          
        if method:
            try:
                method(payload = payload)
            except Exception as e:
                logger.exception("Paystack webhook handler failed - {e}")
                raise ValidationError(f'Error - {e}')
        else:
            logger.error(
                msg = f"Routing - Payment webhook method not found",
            )

        return JsonResponse(data={'status':'success'},status=200)


class StripeWebhookRouteView(APIView, CoinsPurchaseWebhookMixin, MembershipPurchaseWebhookMixin):

    request_category_map = {
        ONLINE_PAYREQUEST_CATEGORY.COINS.value:'coins_purchase_webhook',
        ONLINE_PAYREQUEST_CATEGORY.MEMBERSHIP.value:'membership_purchase_webhook'
    }

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers.get( WEBHOOK_HEADER_KEYWORD[PAYIN_MEDIUM.STRIPE.value] )
        verified_payload = None

        try:
            verified_payload = stripe.Webhook.construct_event(
                payload, sig_header, WEBHOOK_KEY[f'{PAYIN_MEDIUM.STRIPE.value}']
            )
        except ValueError as e:
            raise ValidationError(f'Invalid Payload - {e}')
        except stripe.SignatureVerificationError as e:
            raise ValidationError(f'Invalid Signature - {e}')
        
        verified_payload = normalize_booleans(verified_payload)
        
        session = verified_payload['data']['object']
        request_category = session['metadata'].get('request_category')
        mapped_req_category = self.request_category_map.get(request_category)
        if mapped_req_category:
            method = getattr(self, f"{PAYIN_MEDIUM.STRIPE.value}_{self.request_category_map[request_category]}", None)
            if method:
                try:
                    method(event_payload = verified_payload)
                except Exception as e:
                    logger.exception("Paystack webhook handler failed - {e}")
                    raise ValidationError(f'Error - {e}')
            else:
                logger.error(
                    msg = f"Payment webhook method not found",
                )

        return JsonResponse(data={'status':'success'},status=200)


class FincraWebhookRouteView(APIView, PayoutWebhookMixin):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = generic_webhook_validator(
            request=request, 
            webhook_key = WEBHOOK_KEY[f'{PAYOUT_CHANNEL.FINCRA.value}'],
            header_keyword = WEBHOOK_HEADER_KEYWORD[f'{PAYOUT_CHANNEL.FINCRA.value}']
        )   
        try: 
            return self.fincra_payout_webhook(payload=payload)
        except Exception as e:
            logger.exception("Paystack webhook handler failed - {e}")
            raise ValidationError(f'Error - {e}')
