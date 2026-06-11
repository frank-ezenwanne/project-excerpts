
"""
NB: Please note that these are generic excerpts from a larger codebase protected by NDA
hence some code might be left out.

This file was created because of the seemingly dynamics in dealing with the Flutterwave API

The code below was written for payouts. Flutterwave can payout to various currencies but the 
payload structure varies greatly amongst currencies, with some currencies having fields
1 or 2 nested layers deep. 

Close examination of the docs showed that the currencies have a basic payload structure 
which I placed to be provided by a function get_flutterwave_basepayload rather than a direct 
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
 django model fields using pascal_case, I used a python dict, flutterwave_field_map that maps the flutterwave payload names
 to my django field names to extract the corresponding fields.


 Check the code at the last part of the file for a description on how the payload is built for a currency

"""


def get_flutterwave_basepayload():
    return {
    "bank": {
        "account_number": "",
    },
    "type": ""
}

def get_generic_fwave_payload_edit(): #same edit for multiple currencies
    return {
        "nested_data": {
            "name__first":"", 
            "name__last":"",

            "bank__code":"",
            "bank__branch":""
        },
        "parent_data": {}
    }


        
flutterwave_supported_currencies = {
    'EGP':'Egyptian Pound',
    'ETB':'Ehiopian Birr', 
    'EUR' :'Euro',
    'GBP':'Great Britain Pounds',
    'GHS':'Ghanaian Cedi', 
    'KES': 'Kenyan Shilling',
    'MWK': 'Malawian Kwacha',
    'NGN': 'Nigerian Naira',
    'USD': 'United States Dollar',
    'RWF': 'Rwandan Franc',
    'SLL': 'Sierra Leonean Leone',
    'UGX': 'Ugandan Shilling',
    'XAF': 'Central African CFA',
    'XOF': 'West African CFA',
    'ZAR': 'South African Rand'
}

flutterwave_transfer_edits = {

    'EGP' : {
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "national_identification__type":"",
            "national_identification__identifier":"",
            "national_identification__expiration_date":"",
            "phone__country_code":"",
            "phone__number":"",
            "address__city":"",
            "address__country":"",
            "address__line1":"",
            "address__postal_code":"",
            "address__state":"",
            "bank__code":""
        },
        "parent_data": {}
    },

    'ETB':{
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "bank__code":""
        },
        "parent_data": {}
    },

    'EUR':{
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "phone__country_code":"",
            "phone__number":"",
            "address__city":"",
            "address__country":"",
            "address__line1":"",
            "address__postal_code":"",
            "address__state":"",
            "bank__name":"",
            "bank__swift_code":""
        },
        "parent_data": {"email":""}
    },

    'GBP':{
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "phone__country_code":"",
            "phone__number":"",
            "address__city":"",
            "address__country":"",
            "address__line1":"",
            "address__postal_code":"",
            "address__state":"",
            "bank__name":"",
            "bank__account_type":"",
            "bank__sort_code":""
        },
        "parent_data": {"email":""}
    },

    'GHS': {
        "nested_data": {
            "name__first":"", 
            "name__last":"",

            "bank__code":"",
            "bank__branch":""
        },
        "parent_data": {}
    },

    'KES':{
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "bank__code":""
        },
        "parent_data": {}
    },

    'MWK': {
        "nested_data": {
            "name__first":"", 
            "name__last":"",

            "bank__code":"",
            "bank__branch":""
        },
        "parent_data": {}
    },

    'NGN': {
        "nested_data": {
            "bank__code":"",
        },
        "parent_data": {}
    
    },

    'USD':{
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "phone__country_code":"",
            "phone__number":"",
            "address__city":"",
            "address__country":"",
            "address__line1":"",
            "address__postal_code":"",
            "address__state":"",
            "bank__code":"",
            "bank__account_type":"",
            "bank__routing_number":"",
            "bank__swift_code":""
        },
        "parent_data": {"email":""}
    },

    'RWF':get_generic_fwave_payload_edit(),

    'SLL':get_generic_fwave_payload_edit(),

    'UGX':get_generic_fwave_payload_edit(),

    'XAF':get_generic_fwave_payload_edit(),

    'XOF':get_generic_fwave_payload_edit(),

    'ZAR':{
        "nested_data": {
            "name__first":"", 
            "name__last":"",
            "phone__country_code":"",
            "phone__number":"",
            "address__city":"",
            "address__country":"",
            "address__line1":"",
            "address__postal_code":"",
            "address__state":"",
            "bank__code":""
        },
        "parent_data": {"email":""}
    },
}


flutterwave_field_map = {
        "national_identification__type":"national_identity_type",
        "national_identification__identifier":"national_identity_id",
        "national_identification__expiration_date":"national_identity_expiration_date",
        "phone__country_code":"phone_country_code",
        "phone__number":"phone_number_no_code",
        "address__line1":"address_line1",
        "bank__account_type":"account_type",
    
        "name__first":"beneficiary_first_name", 
        "name__last":"beneficiary_last_name",
        "email":"beneficiary_email",

        "address__city":"beneficiary_city",
        "address__country":"beneficiary_country_code",
        "address__state":"beneficiary_state",
        "address__postal_code":"beneficiary_postal_code",

        "bank__branch":"bank_branch_code",
        "bank__sort_code":"sort_code",
        "bank__code":"bank_code",
        "bank__swift_code":"swift_code",
        "bank__routing_number":"routing_number"
}

flutterwave_verifiable_currencies = ['NGN','GBP','USD']

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
bank_account = 'Bank Account Instance here'

if flutterwave_transfer_edits.get(currency_code): #tries to get the currency from the dict 
    fields_to_set = flutterwave_transfer_edits[currency_code]

nested_elements = fields_to_set['nested_data'] #collects the nested and parent fields in variables
parent_elements = fields_to_set['parent_data']

flutterwave_base_transferpayload = get_flutterwave_basepayload() #create a copy of the base payload
for key in nested_elements:
    if nested_elements[key]: #if there is already a value pick it up !
        value = nested_elements[key]
    else:
        if flutterwave_field_map.get(key): #this block shows how the flutterwave field map is used to get the actual django field name and hence, the value
            value_ref = flutterwave_field_map[key]
            value = getattr(bank_account, value_ref)

    levels = key.split('__') #splitting nested fields on basis of the double underscore splitter
    payload = append_currency_edits(flutterwave_base_transferpayload,levels, value ) #using the recursion algorithm to add the fields
    
for key in parent_elements: #parent fields are added directly to the 1st layer of the base payload
    if parent_elements[key]:
        payload[key] = parent_elements[key]