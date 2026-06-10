from django.conf import settings


"""
NB: Please note that these are generic excerpts from a larger codebase protected by NDA
hence some code might be left out.

This file was created because of the seemingly weird dynamics in dealing with the Fincra API

The code below was written for payouts. Fincra can payout to various currencies but the 
payload structure varies greatly amongst currencies, with some currencies having fields
3 nested layers deep. 

In case you are thinking of creating a payload with all possible fields and nullifying the ones 
that don't apply for a currency, it won't work ! The Fincra API is strict in the sense that
it only allows fields specified by the docs. E.g nullifying bank code for Ghana while slotting in
a value for bank swift code will return an error that might not even match the actual problem (sandbox mode)

Close examination of the docs showed that the all currencies have a basic payload structure 
which I placed to be provided by a function get_fincra_basetransferpayload rather than a direct 
object to prevent memory problems in terms of multiple requests editing the same object in memory.

So I outlined the fields that make each currency unique in a python dict mapping currency
to dicts, nested and parent. The parent data holds fields to be added directly to the first layer of the base payload.
The nested, using a recursion algorithm, uses the double underscore ( __ ) between names to decide where to break into a nested dict.

so beneficiary__address adds 

beneficiary:{
    'address':''
 }

 while beneficiary__address__street adds 

 beneficiary:{
    'address':{
        'street' : ''
    }
 } 

 to the base payload

 Because the payload uses camelCase and field names that might not correspond to the generic bank account
 django model fields using pascal_case, I used a python dict, fincra_field_map that maps the fincra payload names
 to my django field names to extract the corresponding fields.

 Unlike some 3rd parties, Fincra gives freedom to use any of the provided payment schemes of choice to its users. This explains
 the variations for some currencies like USD, GBP, EUR

 Check the code at the last part of the file for a description on how the payload is built for a currency

"""

PAYMENT_SCHEME_FIELD = 'paymentScheme'


def get_fincra_basequote():
    return {
        "action": "send",
        "amount":'',
        "transactionType": "disbursement",
        "sourceCurrency":'USD',
        'business':settings.FINCRA_BUSINESS_ID,
        "destinationCurrency":'',
        "feeBearer": "customer",
        "paymentDestination": "bank_account",
        "beneficiaryType": "individual",
    }
def get_fincra_basetransferpayload():
    return {
        "amount":0,
        "beneficiary": {
            "accountHolderName": "",
            "accountNumber": "",
            "firstName": "",
            "lastName": "",
            "type": "individual"
        },
        
        "business": settings.FINCRA_BUSINESS_ID,
        "customerReference": "",
        "description": "",
        "paymentDestination": "bank_account",
        "sourceCurrency": "USD",
        "sender":{
            "name":"Zenguy",
            "email":settings.FINCRA_EMAIL
        },
    }


fincra_supported_currencies = {
    'NGN':'Nigerian Naira',
    'ZMW':'Zambian Kwacha', 
    'GHS':'Ghanaian Cedi', 
    'KES': 'Kenyan Shilling',
    'GBP':'Great Britain Pounds',
    'EUR' :'Euro',
    'USD': 'United States Dollar'
}

fincra_transfer_edits = {
    'NGN' : {
        "nested_data": {"beneficiary__bankCode":""},
        "parent_data": {"destinationCurrency":"NGN"}
    },
    'ZMW' : {
        "nested_data": {"beneficiary__bankCode":""},
        "parent_data": {"destinationCurrency":"ZMW"}
    },
    'GHS' : {
        "nested_data": {"beneficiary__bankSwiftCode":""} ,
        "parent_data": {"destinationCurrency":"GHS"}
    },

    'KES' : {
        "nested_data": {"beneficiary__bankCode":""} ,
        "parent_data":{"destinationCurrency":"KES"}
    },

    'GBP__FPS' : {
        "nested_data": {
            "beneficiary__sortCode":"",
            "beneficiary__email":"", 
            "beneficiary__country":"",  
        } ,
        "parent_data":{"destinationCurrency":"GBP", "paymentScheme":"fps"}
    },

    'GBP__CHAPS' : {
        "nested_data": {
            "beneficiary__sortCode":"",
            "beneficiary__email":"", 
            "beneficiary__country":"",  
        } ,
        "parent_data":{"destinationCurrency":"GBP", "paymentScheme":"chaps"}
    },

    'EUR__SEPA_INSTANT' : {
        "nested_data": {"beneficiary__country":"", "beneficiary__email":""} ,
        "parent_data":{"destinationCurrency":"EUR", "paymentScheme":"sepa_instant"}
    },

    'EUR__SEPA' : {
        "nested_data": {"beneficiary__country":"", "beneficiary__email":""} ,
        "parent_data":{"destinationCurrency":"EUR", "paymentScheme":"sepa"}
    },

    'USD__SWIFT' : {
        "nested_data": {
            "beneficiary__sortCode":"",
            "beneficiary__email":"", 
            "beneficiary__country":"",  
            "beneficiary__bankSwiftCode":"",  
            "beneficiary__bankName":"",  

            "beneficiary__address__street" :"",
            "beneficiary__address__state" :"",
            "beneficiary__address__city" :"",
            "beneficiary__address__zip" :"",
            "beneficiary__address__country" :"",

            "beneficiary__bankAddress__street" :"",
            "beneficiary__bankAddress__state" :"",
            "beneficiary__bankAddress__city" :"",
            "beneficiary__bankAddress__zip" :"",
            "beneficiary__bankAddress__country" :"",

        } ,
        "parent_data":{"destinationCurrency":"USD", "paymentScheme":"swift", "files":"Cash withdrawal request"}
    },

    'USD__FED_WIRE' : {
        "nested_data": {
            "beneficiary__sortCode":"",
            "beneficiary__email":"", 
            "beneficiary__country":"",  
            "beneficiary__bankCode":"",  
            "beneficiary__bankName":"",  
    
            "beneficiary__address__street" :"",
            "beneficiary__address__state" :"",
            "beneficiary__address__city" :"",
            "beneficiary__address__zip" :"",
            "beneficiary__address__country" :"",

            "beneficiary__bankAddress__street" :"",
            "beneficiary__bankAddress__state" :"",
            "beneficiary__bankAddress__city" :"",
            "beneficiary__bankAddress__zip" :"",
            "beneficiary__bankAddress__country" :"",
        } ,
        "parent_data":{"destinationCurrency":"USD", "paymentScheme":"fed_wire", "files":"Cash withdrawal request"}
    },

    'USD__ACH' : {
        "nested_data": {
            "beneficiary__sortCode":"",
            "beneficiary__email":"", 
            "beneficiary__country":"",  
            "beneficiary__bankCode":"",  
            "beneficiary__bankName":"",  

            "beneficiary__address__street" :"",
            "beneficiary__address__state" :"",
            "beneficiary__address__city" :"",
            "beneficiary__address__zip" :"",
            "beneficiary__address__country" :"",
        } ,
        "parent_data":{"destinationCurrency":"USD", "paymentScheme":"ach", "files":"Cash withdrawal request"}
    },

} 

fincra_field_map = {
    "destinationCurrency": "currency_code",
    "beneficiary__accountHolderName":"bank_account_name",
    "beneficiary__accountNumber":"bank_account_number",
    "beneficiary__bankName":"bank_name",
    "beneficiary__bankSwiftCode":"swift_code",
    "beneficiary__bankCode":"bank_code",
    "beneficiary__sortCode":"sort_code",
    "beneficiary__country":"beneficiary_country_code",
    

    "beneficiary__address__street" :"beneficiary_street",
    "beneficiary__address__state" :"beneficiary_state",
    "beneficiary__address__city" :"beneficiary_city",
    "beneficiary__address__zip" :"beneficiary_zipcode",
    "beneficiary__address__country" :"beneficiary_country_code",

    "beneficiary__bankAddress__street" :"bank_street",
    "beneficiary__bankAddress__state" :"bank_state",
    "beneficiary__bankAddress__city" :"bank_city",
    "beneficiary__bankAddress__zip" :"bank_zipcode",
    "beneficiary__bankAddress__country" :"bank_country_code",
    "beneficiary__firstName":"beneficiary_first_name",
    "beneficiary__lastName":"beneficiary_last_name",
    "beneficiary__email":"beneficiary_email",
    
}



fincra_payscheme_map={
    'GBP':['FPS', 'CHAPS'],
    'EUR':['SEPA', 'SEPA_INSTANT'],
    'USD':['SWIFT','ACH']
}

FINCRA_VERIFIABLE_CURRENCIES = ['NGN','GBP','GHS','EUR']



FINCRA_TRANSFER_SUCCESSFUL = 'successful'
FINCRA_TRANSFER_PROCESSING = 'processing'
FINCRA_TRANSFER_FAILED = 'failed'
FINCRA_LOW_FUNDS_ERROR = 'NO_ENOUGH_MONEY_IN_WALLET'




#utility func that appends the pieces to the base payload with basic recursion
def append_currency_edits(base_dict,keys, value ):

    if not keys:
        return base_dict

    current_key = keys[0]

    if len(keys) == 1:
        base_dict[current_key] = value
    else:
        if current_key not in base_dict or not isinstance(base_dict[current_key], dict):
            base_dict[current_key] = {}
        append_currency_edits(base_dict[current_key],keys[1:], value)

    return base_dict



# The code below shows an example of the payload build in action with the help of the append_currency_edits function
currency_code = 'GBP'
payment_scheme = 'FPS'
bank_account = 'Bank Account Instance here'

if fincra_transfer_edits.get(currency_code): #tries to get the currency from the dict else it uses the currency joined with payscheme if provided
    fields_to_set = fincra_transfer_edits[currency_code]
elif payment_scheme and fincra_transfer_edits.get(f'{currency_code}__{payment_scheme}'):
    fields_to_set = fincra_transfer_edits[f'{currency_code}__{payment_scheme}']

nested_elements = fields_to_set['nested_data'] #collects the nested and parent fields in variables
parent_elements = fields_to_set['parent_data']

fincra_base_transferpayload = get_fincra_basetransferpayload() #create a copy of the base payload
for key in nested_elements:
    if nested_elements[key]: #if there is already a value pick it up !
        value = nested_elements[key]
    else:
        if fincra_field_map.get(key): #this block shows how the fincra field map is used to get the actual django field name and hence, the value
            value_ref = fincra_field_map[key]
            value = getattr(bank_account, value_ref)

    levels = key.split('__') #splitting nested fields on basis of the double underscore splitter
    payload = append_currency_edits(fincra_base_transferpayload,levels, value ) #using the recursion algorithm to add the fields
    
for key in parent_elements: #parent fields are added directly to the 1st layer of the base payload
    if parent_elements[key]:
        payload[key] = parent_elements[key]

#beneficiary nested object is updated separately as there are common fields as specified in the base payload, hence will be skipped by the above 
benef_data = fincra_base_transferpayload['beneficiary']
payload_benef_data = payload['beneficiary'] #bring beneficiary out to update it..still linked in memory though
for benef_field in benef_data:
    if not benef_data[benef_field]:
        map_field = f'beneficiary__{benef_field}'
        if fincra_field_map.get(map_field):
            payload_benef_data[benef_field] = getattr(bank_account, fincra_field_map[map_field]) #this line shows how the fincra field map is used to get the actual django field name and hence, the value
   