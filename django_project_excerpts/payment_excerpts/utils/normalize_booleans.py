"""
Booleans passed into the metadata of paystack and stripe usually come back as strings.
This gets the booleans back !
"""
def normalize_booleans(obj):
    if isinstance(obj, dict):
        return {k: normalize_booleans(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize_booleans(v) for v in obj]
    if isinstance(obj, str):
        low = obj.strip().lower()
        if low == 'true':
            return True
        if low == 'false':
            return False
    return obj