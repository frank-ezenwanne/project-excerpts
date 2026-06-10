import hmac
import hashlib
import json
from rest_framework.exceptions import ValidationError
from .normalize_booleans import normalize_booleans
from logging import getLogger
logger = getLogger("django_server")

"""
This is a generic webhook signature validator used by fincra and paystack.
A boolean normalizer was added to convert the strings in the metadata back to booleans 
if they are supposed to be
"""

def generic_webhook_validator( request, webhook_key, header_keyword ): 
        raw_payload = request.body
        #encode the webhook key and save it in a variable..webhook key is secret key for some 3rd parties
        key = webhook_key.encode("utf-8")
        
        #encrypt the payload
        expected_signature = hmac.new(key, raw_payload, hashlib.sha512).hexdigest()

        #get the signature from the header
        request_header_signature = request.headers.get(header_keyword)
        if not request_header_signature:
            logger.error(f"Missing webhook signature header: {header_keyword}")
            raise ValidationError('Missing signature !')
        
        #check signature authencity
        if hmac.compare_digest(request_header_signature, expected_signature):
            try:
                payload = json.loads(raw_payload.decode('utf-8'))
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON payload")
                raise ValidationError('Invalid JSON when decoding')


            payload = normalize_booleans(payload)
            return payload
        else:
            logger.error(f"Webhook signature mismatch. Expected: {expected_signature}, Got: {request_header_signature}, Header key: {header_keyword}")
            raise ValidationError('Invalid request !')