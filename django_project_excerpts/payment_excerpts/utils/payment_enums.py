from django.db import models

class PAYIN_MEDIUM(models.TextChoices):
        PAYSTACK = 'paystack', 'paystack'
        STRIPE = 'stripe', 'stripe'
        FINCRA = 'fincra', 'fincra'
        LOCAL = 'local', 'local'

class PAYOUT_CHANNEL(models.TextChoices):
        PAYSTACK = 'paystack', 'paystack'
        FINCRA = 'fincra', 'fincra'
        MANUAL = 'manual' , 'manual'

#Merge existing choices tuples into a flat list of (Value, Label)
raw_combined = list(PAYIN_MEDIUM.choices) + list(PAYOUT_CHANNEL.choices)

#Build a valid mapping dictionary
member_map = {}
labels_map = {}

for val, label in raw_combined:
    attr_name = str(val).upper().replace('-', '_').replace(' ', '_')
    member_map[attr_name] = val
    labels_map[val] = label  # Store labels temporarily to bind later


ALL_PAYMENT_PLATFORMS = models.TextChoices('ALL_PAYMENT_PLATFORMS', member_map)

# Re-bind the human-readable labels to match original choices
for member in ALL_PAYMENT_PLATFORMS:
    member._label_ = labels_map.get(member.value, member.name)


class ONLINE_PAYMENT_STATUS(models.TextChoices):
        PENDING = 'pending', 'pending'
        PAID = 'paid', 'paid'
        OTHER = ('other', 'other')
        INVALIDATED = 'invalidated', 'invalidated'


class ONLINE_PURCHASE_ORDER_STATUS(models.TextChoices):
        PENDING = ('pending', 'pending')
        COMPLETED = ('completed', 'completed')
        INVALIDATED = ('invalidated', 'invalidated')
    
class STRIPE_EVENTS(models.TextChoices):
       CHECKOUT_COMPLETED = ('checkout.session.completed','checkout.session.completed')
       PAYMENT_INTENT_SUCCEEDED = ('payment_intent.succeeded','payment_intent.succeeded')

class PAYSTACK_EVENTS(models.TextChoices):
       CHARGE_SUCCESS = ('charge.success', 'charge.success')
       TRANSFER_SUCCESS = ('transfer.success', 'transfer.success')
       TRANSFER_FAILED = ('transfer.failed', 'transfer.failed')
    
class PAYSTACK_TRANSACTION_STATUS(models.TextChoices):
        ABANDONED = ('abandoned', 'abandoned')
        FAILED =    ('failed', 'failed')
        ONGOING = ('ongoing', 'ongoing')
        PENDING = ('pending', 'pending')
        PROCESSING = ('processing', 'processing')
        QUEUED = ('queued', 'queued')
        REVERSED = ('reversed', 'reversed')
        SUCCESS = ('success', 'success')

PENDING_PAYSTACK_STATUS = (
        PAYSTACK_TRANSACTION_STATUS.ABANDONED.value,
        PAYSTACK_TRANSACTION_STATUS.ONGOING.value,
        PAYSTACK_TRANSACTION_STATUS.PENDING.value,
        PAYSTACK_TRANSACTION_STATUS.PROCESSING.value,
)

OTHER_PAYSTACK_STATUS = (
        PAYSTACK_TRANSACTION_STATUS.QUEUED.value,
        PAYSTACK_TRANSACTION_STATUS.REVERSED.value,
)

class ONLINE_PAYREQUEST_CATEGORY(models.TextChoices):
        COINS = ('coins', 'coins')
        MEMBERSHIP = ('membership_subscription', 'membership_subscription')

class PAYMENT_TRANSFER_SCHEMES(models.TextChoices):
        FPS = ('FPS', 'FPS')
        SEPA = ('SEPA','SEPA')
        SEPA_INSTANT = ('SEPA_INSTANT','SEPA_INSTANT')
        SWIFT = ('SWIFT','SWIFT')
        ACH = ('ACH', 'ACH')
        FED_WIRE = ('FED_WIRE', 'FED_WIRE')

class AUTO_WITHDRAWAL_STATUS(models.TextChoices):
       INITIATED =  ('initiated', 'initiated') #just created on db, not yet linked (specific fields filled) with the withdraw transaction
       PROCESSING = ('processing', 'processing') #linked to the online transaction, fields e.g transaction id filled , still processing
       COMPLETED = ('completed', 'completed') #transfer is completed
       FAILED = ('failed', 'failed') #transfer failed

class AUTO_REFUND_STATUS(models.TextChoices):
       INITIATED =  ('initiated', 'initiated') #just created on db, not yet linked (specific fields filled) with the withdraw transaction
       PROCESSING = ('processing', 'processing') #linked to the online transaction, fields e.g transaction id filled , still processing
       COMPLETED = ('completed', 'completed') #transfer is completed
       FAILED = ('failed', 'failed') #transfer failed
    
class PAYOUT_ACTION(models.TextChoices):
        WITHDRAWAL = ('withdrawal', 'withdrawal')
        REFUND = ('refund', 'refund')

class MEMBERSHIP_SUB_PAYLOAD_TYPE(models.TextChoices):
        INITIAL_SUB = ('initial_subscription', 'initial_subscription')
        RENEWAL = ('renewal', 'renewal')


class PAYMENT_SCHEME_CHOICES(models.TextChoices):
        FPS = ('FPS', 'FPS')
        SEPA = ('SEPA','SEPA')
        SEPA_INSTANT = ('SEPA_INSTANT','SEPA_INSTANT')
        SWIFT = ('SWIFT','SWIFT')
        ACH = ('ACH', 'ACH')
        FED_WIRE = ('FED_WIRE', 'FED_WIRE')
    
class FINCRA_EVENTS(models.TextChoices):
        PAYOUT_SUCCESS = ('payout.successful','payout.successful')
        PAYOUT_FAILED = ('payout.failed','payout.failed')
